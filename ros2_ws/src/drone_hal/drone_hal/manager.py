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
Hardware Manager: orchestrates registry, loader, discovery, and DI.

It is itself a LifecycleComponent so a single object can be driven by
the ROS 2 node's lifecycle callbacks (see node.py). Driver classes
resolved by IDriverLoader are expected to accept a single
``DeviceDescriptor`` positional argument, i.e. ``DriverCls(descriptor)``.
This is the one convention drone_hal imposes on every driver package.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging as _stdlib_logging

from drone_hal.device import DeviceConnectivity, DeviceDescriptor
from drone_hal.discovery import IDeviceDiscovery
from drone_hal.driver import IHardwareDriver
from drone_hal.loader import IDriverLoader
from drone_hal.registry import IHardwareRegistry
from drone_interfaces.diagnostics import DiagnosticItem, DiagnosticLevel, DiagnosticReport
from drone_interfaces.health import HealthStatus
from drone_interfaces.lifecycle import LifecycleComponent, LifecycleState

_LOG = _stdlib_logging.getLogger('drone_hal.manager')

_HEALTH_TO_DIAGNOSTIC = {
    HealthStatus.OK: DiagnosticLevel.OK,
    HealthStatus.DEGRADED: DiagnosticLevel.WARN,
    HealthStatus.WARNING: DiagnosticLevel.WARN,
    HealthStatus.CRITICAL: DiagnosticLevel.ERROR,
    HealthStatus.UNKNOWN: DiagnosticLevel.STALE,
}


@dataclass(frozen=True)
class DeviceOperationResult:
    """Outcome of a lifecycle fan-out operation for one device."""

    device_id: str
    success: bool
    detail: str = ''


class HardwareManager(LifecycleComponent):
    """Owns and drives every registered hardware device's lifecycle."""

    def __init__(
        self,
        registry: IHardwareRegistry,
        loader: IDriverLoader,
        discovery: IDeviceDiscovery,
        descriptors: list[DeviceDescriptor],
    ) -> None:
        self._registry = registry
        self._loader = loader
        self._discovery = discovery
        self._descriptors = descriptors
        self._state = LifecycleState.UNCONFIGURED
        self._connectivity: dict[str, DeviceConnectivity] = {}

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    @property
    def registry(self) -> IHardwareRegistry:
        return self._registry

    def on_configure(self) -> bool:
        for descriptor in self._descriptors:
            driver_cls = self._loader.load(descriptor.driver_class)
            self._registry.register(descriptor, lambda d=descriptor, c=driver_cls: c(d))
        self._connectivity = self._discovery.scan(self._descriptors)
        self._state = LifecycleState.INACTIVE
        return True

    def on_activate(self) -> bool:
        results = self._fan_out('on_activate')
        self._state = LifecycleState.ACTIVE
        return all(r.success for r in results)

    def on_deactivate(self) -> bool:
        results = self._fan_out('on_deactivate')
        self._state = LifecycleState.INACTIVE
        return all(r.success for r in results)

    def on_cleanup(self) -> bool:
        for descriptor in self._descriptors:
            self._registry.unregister(descriptor.device_id)
        self._connectivity = {}
        self._state = LifecycleState.UNCONFIGURED
        return True

    def on_shutdown(self) -> bool:
        results = self._fan_out('on_shutdown')
        self._state = LifecycleState.FINALIZED
        return all(r.success for r in results)

    def on_error(self, error: Exception) -> bool:
        _LOG.error('hardware manager fault: %s', error)
        return False

    def rediscover(self) -> dict[str, DeviceConnectivity]:
        """Re-scan bus presence for all configured devices without changing lifecycle state."""
        self._connectivity = self._discovery.scan(self._descriptors)
        return dict(self._connectivity)

    def collect_diagnostics(self) -> list[DiagnosticReport]:
        """Return one DiagnosticReport per instantiated device driver."""
        reports: list[DiagnosticReport] = []
        for device_id in self._registry.instantiated_devices():
            driver = self._registry.get(device_id)
            reports.append(self._to_diagnostic_report(driver))
        return reports

    def _fan_out(self, hook_name: str) -> list[DeviceOperationResult]:
        results: list[DeviceOperationResult] = []
        for descriptor in self._descriptors:
            driver = self._registry.get(descriptor.device_id)
            hook = getattr(driver, hook_name)
            try:
                success = hook()
                results.append(DeviceOperationResult(descriptor.device_id, bool(success)))
            except Exception as exc:  # noqa: BLE001 - isolate one device's fault from the rest
                driver.on_error(exc)
                results.append(DeviceOperationResult(descriptor.device_id, False, str(exc)))
        return results

    @staticmethod
    def _to_diagnostic_report(driver: IHardwareDriver) -> DiagnosticReport:
        report = driver.check_health()
        return DiagnosticReport(
            name=driver.descriptor.device_id,
            level=_HEALTH_TO_DIAGNOSTIC[report.status],
            message=report.message,
            hardware_id=driver.descriptor.address,
            items=tuple(
                DiagnosticItem(key=key, value=str(value))
                for key, value in report.metrics.items()
            ),
        )
