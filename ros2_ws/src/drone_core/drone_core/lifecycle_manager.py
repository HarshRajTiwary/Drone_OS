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
LifecycleManager fans out lifecycle transitions across named core services.

Isolates one service's failure (health monitor, mission registry, ...)
from the others. Same design as drone_hal.manager.HardwareManager's
device fan-out, applied to core services instead of hardware drivers.
"""

from __future__ import annotations

from dataclasses import dataclass

from drone_interfaces.lifecycle import LifecycleComponent, LifecycleState


@dataclass(frozen=True)
class ComponentOperationResult:
    """Outcome of a lifecycle fan-out operation for one named component."""

    name: str
    success: bool
    detail: str = ''


class LifecycleManager(LifecycleComponent):
    """Drives a named set of LifecycleComponents through configure/activate/shutdown."""

    def __init__(self, components: dict[str, LifecycleComponent]) -> None:
        self._components = components
        self._state = LifecycleState.UNCONFIGURED

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    def component(self, name: str) -> LifecycleComponent:
        return self._components[name]

    def on_configure(self) -> bool:
        results = self._fan_out('on_configure')
        self._state = LifecycleState.INACTIVE
        return all(r.success for r in results)

    def on_activate(self) -> bool:
        results = self._fan_out('on_activate')
        self._state = LifecycleState.ACTIVE
        return all(r.success for r in results)

    def on_deactivate(self) -> bool:
        results = self._fan_out('on_deactivate')
        self._state = LifecycleState.INACTIVE
        return all(r.success for r in results)

    def on_cleanup(self) -> bool:
        results = self._fan_out('on_cleanup')
        self._state = LifecycleState.UNCONFIGURED
        return all(r.success for r in results)

    def on_shutdown(self) -> bool:
        results = self._fan_out('on_shutdown')
        self._state = LifecycleState.FINALIZED
        return all(r.success for r in results)

    def on_error(self, error: Exception) -> bool:
        return False

    def _fan_out(self, hook_name: str) -> list[ComponentOperationResult]:
        results: list[ComponentOperationResult] = []
        for name, component in self._components.items():
            hook = getattr(component, hook_name)
            try:
                success = hook()
                results.append(ComponentOperationResult(name, bool(success)))
            except Exception as exc:  # noqa: BLE001 - isolate one component's fault from the rest
                component.on_error(exc)
                results.append(ComponentOperationResult(name, False, str(exc)))
        return results
