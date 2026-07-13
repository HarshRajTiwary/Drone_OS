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
Shared test doubles for drone_hal's unit tests.

Not a test_*.py module itself, so pytest does not collect it directly.
"""

from __future__ import annotations

from drone_hal.device import DeviceConnectivity, DeviceDescriptor
from drone_hal.driver import IHardwareDriver
from drone_interfaces.health import HealthReport, HealthStatus
from drone_interfaces.lifecycle import LifecycleState


class FakeDriver(IHardwareDriver):
    """Minimal concrete IHardwareDriver used across drone_hal's unit tests."""

    def __init__(self, descriptor: DeviceDescriptor, fail_on: str | None = None) -> None:
        self._descriptor = descriptor
        self._state = LifecycleState.UNCONFIGURED
        self._connectivity = DeviceConnectivity.PRESENT
        self._fail_on = fail_on
        self.calls: list[str] = []

    @property
    def descriptor(self) -> DeviceDescriptor:
        return self._descriptor

    @property
    def connectivity(self) -> DeviceConnectivity:
        return self._connectivity

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    def _run(self, name: str, next_state: LifecycleState) -> bool:
        self.calls.append(name)
        if self._fail_on == name:
            raise RuntimeError(f'{name} failed for {self._descriptor.device_id}')
        self._state = next_state
        return True

    def on_configure(self) -> bool:
        return self._run('on_configure', LifecycleState.INACTIVE)

    def on_activate(self) -> bool:
        return self._run('on_activate', LifecycleState.ACTIVE)

    def on_deactivate(self) -> bool:
        return self._run('on_deactivate', LifecycleState.INACTIVE)

    def on_cleanup(self) -> bool:
        return self._run('on_cleanup', LifecycleState.UNCONFIGURED)

    def on_shutdown(self) -> bool:
        return self._run('on_shutdown', LifecycleState.FINALIZED)

    def on_error(self, error: Exception) -> bool:
        self.calls.append('on_error')
        return False

    def reconnect(self) -> bool:
        self._connectivity = DeviceConnectivity.PRESENT
        return True

    def check_health(self) -> HealthReport:
        return HealthReport(
            component=self._descriptor.device_id,
            status=HealthStatus.OK,
            message='fake nominal',
            timestamp=0.0,
            metrics={'reads': 1.0},
        )
