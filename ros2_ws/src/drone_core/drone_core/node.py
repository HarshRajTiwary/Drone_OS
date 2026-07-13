# Copyright 2026 DroneOS Platform Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
DroneCoreNode: the ROS 2 node running the Phase 1 boot sequence.

Wraps BootManager, adds the ROS-graph health check, publishes
SystemState (drone_msgs) and diagnostics (diagnostic_msgs), and serves
the mission ActivateMission/DeactivateMission/ListMissions services.
This is a plain rclpy.Node, not a LifecycleNode: the boot sequence itself
already implements the requested lifecycle (BOOTING -> INITIALIZING ->
READY) via BootManager/CoreStateMachine, so a second ROS-level lifecycle
layered on top would just duplicate it.
"""

from __future__ import annotations

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from drone_core.boot_manager import BootManager
from drone_core.health_checks import RosGraphHealthCheck
from drone_interfaces.diagnostics import DiagnosticItem, DiagnosticLevel, DiagnosticReport
from drone_interfaces.exceptions import MissionError
from drone_interfaces.health import HealthStatus
from drone_msgs.msg import MissionInfo
from drone_msgs.srv import ActivateMission, DeactivateMission, ListMissions
import rclpy
from rclpy.node import Node

_HEALTH_TO_DIAGNOSTIC = {
    HealthStatus.OK: DiagnosticLevel.OK,
    HealthStatus.DEGRADED: DiagnosticLevel.WARN,
    HealthStatus.WARNING: DiagnosticLevel.WARN,
    HealthStatus.CRITICAL: DiagnosticLevel.ERROR,
    HealthStatus.UNKNOWN: DiagnosticLevel.STALE,
}


def _to_diagnostic_report(report) -> DiagnosticReport:
    return DiagnosticReport(
        name=report.component,
        level=_HEALTH_TO_DIAGNOSTIC[report.status],
        message=report.message,
        items=tuple(
            DiagnosticItem(key=k, value=str(v)) for k, v in report.metrics.items()
        ),
    )


def _to_diagnostic_array(reports: list[DiagnosticReport]) -> DiagnosticArray:
    array = DiagnosticArray()
    for report in reports:
        status = DiagnosticStatus()
        status.name = report.name
        status.level = bytes([int(report.level)])
        status.message = report.message
        status.hardware_id = report.hardware_id
        status.values = [KeyValue(key=item.key, value=item.value) for item in report.items]
        array.status.append(status)
    return array


class DroneCoreNode(Node):
    """Runs the DroneOS Core boot sequence and serves mission/diagnostics interfaces."""

    def __init__(self) -> None:
        super().__init__('drone_core_node')
        self.declare_parameter('config_dir', '')
        self.declare_parameter('diagnostics_period_s', 1.0)

        config_dir = self.get_parameter('config_dir').value
        self._boot_manager = BootManager(config_dir, node_name='drone_core')
        self._boot_manager.health_monitor.register(RosGraphHealthCheck(self))

        self._diagnostics_pub = self.create_publisher(DiagnosticArray, '/diagnostics', 10)

        self.create_service(ActivateMission, '/drone_core/activate_mission', self._on_activate)
        self.create_service(
            DeactivateMission, '/drone_core/deactivate_mission', self._on_deactivate,
        )
        self.create_service(ListMissions, '/drone_core/list_missions', self._on_list_missions)

        if not self._boot_manager.boot():
            self.get_logger().error('drone_core boot sequence failed')
        else:
            self.get_logger().info('drone_core READY')

        period = self.get_parameter('diagnostics_period_s').value
        self.create_timer(period, self._publish_diagnostics)

    def _publish_diagnostics(self) -> None:
        self._boot_manager.health_monitor.heartbeat.beat()
        reports = [_to_diagnostic_report(r) for r in self._boot_manager.health_monitor.collect()]
        self._diagnostics_pub.publish(_to_diagnostic_array(reports))

    def _on_activate(self, request, response):
        try:
            response.success = self._boot_manager.mission_registry.activate(
                request.mission_name, {'config_yaml': request.config_yaml},
            )
            response.message = f'{request.mission_name} activated'
        except MissionError as exc:
            response.success = False
            response.message = str(exc)
        return response

    def _on_deactivate(self, request, response):
        response.success = self._boot_manager.mission_registry.deactivate(request.mission_name)
        response.message = (
            f'{request.mission_name} deactivated' if response.success
            else f'{request.mission_name} was not active'
        )
        return response

    def _on_list_missions(self, request, response):
        response.missions = [
            MissionInfo(name=m.name, version=m.version, description=m.description)
            for m in self._boot_manager.mission_registry.discover()
        ]
        return response


def main(args: list[str] | None = None) -> None:
    """Entry point for the drone_core_node console script."""
    rclpy.init(args=args)
    node = DroneCoreNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
