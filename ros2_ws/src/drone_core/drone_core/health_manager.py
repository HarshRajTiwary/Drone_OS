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
CoreHealthMonitor implements IHealthMonitor and LifecycleComponent.

Driven by LifecycleManager the same way drone_hal drives hardware
drivers. on_configure() registers the stdlib-only CPU/RAM/disk/heartbeat
checks; a ROS-graph check is added separately once an rclpy node exists
(see node.py), since this class must stay constructible without ROS.
"""

from __future__ import annotations

from typing import Any

from drone_core.health_checks import (
    CpuHealthCheck,
    DiskHealthCheck,
    HeartbeatHealthCheck,
    RamHealthCheck,
)
from drone_interfaces.health import HealthReport, HealthStatus, IHealthCheckable, IHealthMonitor
from drone_interfaces.lifecycle import LifecycleComponent, LifecycleState

_STATUS_ORDER = [
    HealthStatus.OK, HealthStatus.DEGRADED, HealthStatus.WARNING,
    HealthStatus.CRITICAL, HealthStatus.UNKNOWN,
]

_DEFAULT_THRESHOLDS = {'degraded_percent': 70.0, 'warn_percent': 85.0, 'critical_percent': 95.0}


class CoreHealthMonitor(IHealthMonitor, LifecycleComponent):
    """Aggregates health across CPU, RAM, disk, heartbeat, and any registered checks."""

    def __init__(self, safety_config: dict[str, Any] | None = None) -> None:
        self._components: dict[str, IHealthCheckable] = {}
        self._state = LifecycleState.UNCONFIGURED
        health_config = (safety_config or {}).get('health', {})
        self._cpu_thresholds = {**_DEFAULT_THRESHOLDS, **health_config.get('cpu', {})}
        self._ram_thresholds = {**_DEFAULT_THRESHOLDS, **health_config.get('ram', {})}
        self._disk_thresholds = {**_DEFAULT_THRESHOLDS, **health_config.get('disk', {})}
        stale_after_s = health_config.get('heartbeat', {}).get('stale_after_s', 5.0)
        self.heartbeat = HeartbeatHealthCheck(stale_after_s=stale_after_s)

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    def register(self, component: IHealthCheckable) -> None:
        report = component.check_health()
        self._components[report.component] = component

    def unregister(self, component_name: str) -> None:
        self._components.pop(component_name, None)

    def collect(self) -> list[HealthReport]:
        return [component.check_health() for component in self._components.values()]

    def overall_status(self) -> HealthStatus:
        reports = self.collect()
        if not reports:
            return HealthStatus.UNKNOWN
        return max(reports, key=lambda r: _STATUS_ORDER.index(r.status)).status

    def on_configure(self) -> bool:
        self.register(CpuHealthCheck(**self._cpu_thresholds))
        self.register(RamHealthCheck(**self._ram_thresholds))
        self.register(DiskHealthCheck(**self._disk_thresholds))
        self.register(self.heartbeat)
        self._state = LifecycleState.INACTIVE
        return True

    def on_activate(self) -> bool:
        self.heartbeat.beat()
        self._state = LifecycleState.ACTIVE
        return True

    def on_deactivate(self) -> bool:
        self._state = LifecycleState.INACTIVE
        return True

    def on_cleanup(self) -> bool:
        self._components.clear()
        self._state = LifecycleState.UNCONFIGURED
        return True

    def on_shutdown(self) -> bool:
        self._state = LifecycleState.FINALIZED
        return True

    def on_error(self, error: Exception) -> bool:
        return False
