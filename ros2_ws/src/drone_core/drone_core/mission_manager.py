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
CoreMissionRegistry: implements drone_interfaces.mission_registry.IMissionRegistry.

Registration, discovery, activation, and deactivation only — no mission
logic. Concrete missions (e.g. QR precision landing) register a factory
here from outside this package; drone_core never imports a mission
plugin.
"""

from __future__ import annotations

from typing import Any

from drone_interfaces.exceptions import MissionError
from drone_interfaces.lifecycle import LifecycleComponent, LifecycleState
from drone_interfaces.mission import IMissionPlugin, MissionMetadata, MissionState
from drone_interfaces.mission_registry import IMissionRegistry, MissionFactory


class CoreMissionRegistry(IMissionRegistry, LifecycleComponent):
    """In-memory mission plugin registry; at most one mission active at a time."""

    def __init__(self) -> None:
        self._factories: dict[str, tuple[MissionFactory, MissionMetadata]] = {}
        self._active: IMissionPlugin | None = None
        self._state = LifecycleState.UNCONFIGURED

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    def register(self, factory: MissionFactory, metadata: MissionMetadata) -> None:
        if metadata.name in self._factories:
            raise MissionError(f'{metadata.name} is already registered')
        self._factories[metadata.name] = (factory, metadata)

    def discover(self) -> list[MissionMetadata]:
        return [metadata for _, metadata in self._factories.values()]

    def activate(self, name: str, config: dict[str, Any]) -> bool:
        if name not in self._factories:
            raise MissionError(f'unknown mission {name!r}')
        if self._active is not None:
            raise MissionError(
                f'{self._active.metadata.name} is already active; deactivate it first',
            )
        factory, _ = self._factories[name]
        plugin = factory()
        plugin.initialize(config)
        plugin.start()
        self._active = plugin
        return True

    def deactivate(self, name: str) -> bool:
        if self._active is None or self._active.metadata.name != name:
            return False
        self._active.shutdown()
        self._active = None
        return True

    def active_mission(self) -> IMissionPlugin | None:
        return self._active

    def mission_state(self, name: str) -> MissionState:
        if self._active is not None and self._active.metadata.name == name:
            return self._active.state
        return MissionState.UNINITIALIZED

    def on_configure(self) -> bool:
        self._state = LifecycleState.INACTIVE
        return True

    def on_activate(self) -> bool:
        self._state = LifecycleState.ACTIVE
        return True

    def on_deactivate(self) -> bool:
        if self._active is not None:
            self.deactivate(self._active.metadata.name)
        self._state = LifecycleState.INACTIVE
        return True

    def on_cleanup(self) -> bool:
        self._factories.clear()
        self._state = LifecycleState.UNCONFIGURED
        return True

    def on_shutdown(self) -> bool:
        if self._active is not None:
            self.deactivate(self._active.metadata.name)
        self._state = LifecycleState.FINALIZED
        return True

    def on_error(self, error: Exception) -> bool:
        return False
