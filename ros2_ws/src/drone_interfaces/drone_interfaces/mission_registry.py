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
Mission registry contract: registration and discovery only, no mission logic.

drone_core's Mission Manager implements IMissionRegistry to register plugin
factories, discover available missions, and activate/deactivate at most one
mission at a time. It never contains mission-specific behavior itself.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from drone_interfaces.mission import IMissionPlugin, MissionMetadata, MissionState

MissionFactory = Callable[[], IMissionPlugin]


class IMissionRegistry(ABC):
    """Contract for registering, discovering, and activating mission plugins."""

    @abstractmethod
    def register(self, factory: MissionFactory, metadata: MissionMetadata) -> None:
        """
        Register a mission plugin factory under ``metadata.name``.

        Raises MissionError if a plugin with the same name is already
        registered.
        """

    @abstractmethod
    def discover(self) -> list[MissionMetadata]:
        """Return metadata for every registered mission plugin."""

    @abstractmethod
    def activate(self, name: str, config: dict[str, Any]) -> bool:
        """
        Instantiate, initialize, and start the named mission.

        Raises MissionError if ``name`` is unknown or another mission is
        already active.
        """

    @abstractmethod
    def deactivate(self, name: str) -> bool:
        """Shut down the named mission if it is currently active."""

    @abstractmethod
    def active_mission(self) -> IMissionPlugin | None:
        """Return the currently active mission plugin instance, if any."""

    @abstractmethod
    def mission_state(self, name: str) -> MissionState:
        """Return the current state of the named mission."""
