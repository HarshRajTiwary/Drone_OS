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
HardwareManagerNode: the ROS 2 lifecycle node wrapping HardwareManager.

Device descriptors are loaded from a YAML file referenced by the
``devices_config_path`` parameter (see config/hal_devices.yaml). Standard
diagnostic_msgs are used for /diagnostics rather than a drone_hal-specific
message type, since drone_msgs (Phase 1 package 2) does not exist yet and
diagnostic_msgs already covers this need without introducing a dependency
on an unbuilt package.
"""

from __future__ import annotations

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from drone_hal.device import BusType, DeviceDescriptor
from drone_hal.discovery import DeviceDiscovery
from drone_hal.loader import DriverLoader
from drone_hal.manager import HardwareManager
from drone_hal.registry import HardwareRegistry
import rclpy
from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn
import yaml


def _load_descriptors(config_path: str) -> list[DeviceDescriptor]:
    if not config_path:
        return []
    with open(config_path, encoding='utf-8') as config_file:
        raw = yaml.safe_load(config_file) or {}
    return [
        DeviceDescriptor(
            device_id=entry['device_id'],
            device_type=entry['device_type'],
            bus=BusType(entry['bus']),
            address=entry['address'],
            driver_class=entry['driver_class'],
            metadata=entry.get('metadata', {}),
        )
        for entry in raw.get('devices', [])
    ]


def _to_diagnostic_array(reports) -> DiagnosticArray:
    array = DiagnosticArray()
    for report in reports:
        status = DiagnosticStatus()
        status.name = report.name
        status.level = bytes([int(report.level)])
        status.message = report.message
        status.hardware_id = report.hardware_id
        status.values = [
            KeyValue(key=item.key, value=item.value) for item in report.items
        ]
        array.status.append(status)
    return array


class HardwareManagerNode(LifecycleNode):
    """Lifecycle node that owns and drives the HAL's HardwareManager."""

    def __init__(self) -> None:
        super().__init__('hardware_manager_node')
        self.declare_parameter('devices_config_path', '')
        self.declare_parameter('diagnostics_period_s', 1.0)
        self._manager: HardwareManager | None = None
        self._diagnostics_publisher = None
        self._diagnostics_timer = None
        self.get_logger().info('drone_hal hardware_manager_node started')

    def on_configure(self, state) -> TransitionCallbackReturn:
        config_path = self.get_parameter('devices_config_path').value
        descriptors = _load_descriptors(config_path)
        self._manager = HardwareManager(
            registry=HardwareRegistry(),
            loader=DriverLoader(),
            discovery=DeviceDiscovery(),
            descriptors=descriptors,
        )
        if not self._manager.on_configure():
            return TransitionCallbackReturn.FAILURE

        self._diagnostics_publisher = self.create_lifecycle_publisher(
            DiagnosticArray, '/diagnostics', 10,
        )
        self.get_logger().info(
            f'drone_hal configured with {len(descriptors)} device(s)',
        )
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state) -> TransitionCallbackReturn:
        if not self._manager.on_activate():
            return TransitionCallbackReturn.FAILURE
        period = self.get_parameter('diagnostics_period_s').value
        self._diagnostics_timer = self.create_timer(period, self._publish_diagnostics)
        return super().on_activate(state)

    def on_deactivate(self, state) -> TransitionCallbackReturn:
        if self._diagnostics_timer is not None:
            self._diagnostics_timer.cancel()
            self._diagnostics_timer = None
        self._manager.on_deactivate()
        return super().on_deactivate(state)

    def on_cleanup(self, state) -> TransitionCallbackReturn:
        self._manager.on_cleanup()
        self._manager = None
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state) -> TransitionCallbackReturn:
        if self._manager is not None:
            self._manager.on_shutdown()
        return TransitionCallbackReturn.SUCCESS

    def _publish_diagnostics(self) -> None:
        if self._manager is None or self._diagnostics_publisher is None:
            return
        reports = self._manager.collect_diagnostics()
        self._diagnostics_publisher.publish(_to_diagnostic_array(reports))


def main(args: list[str] | None = None) -> None:
    """Entry point for the hardware_manager_node console script."""
    rclpy.init(args=args)
    node = HardwareManagerNode()
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
