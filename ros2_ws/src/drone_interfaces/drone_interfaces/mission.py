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
Mission plugin contract, per docs/interfaces/mission_interface.md.

Defines the lifecycle every mission plugin must implement. This package
contains no mission logic: Phase 1 implements only the contract and the
registry that hosts it (see mission_registry.py); concrete missions such as
QR precision landing are out of scope until a later phase.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


class MissionState(Enum):
    """Lifecycle state of a single mission plugin instance."""

    UNINITIALIZED = auto()
    INITIALIZED = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    ABORTED = auto()
    FAILED = auto()


@dataclass(frozen=True)
class MissionMetadata:
    """Static identity of a mission plugin, used for discovery and registration."""

    name: str
    version: str
    description: str
    author: str = ''


class IMissionPlugin(ABC):
    """Contract that every DroneOS mission plugin must satisfy."""

    @property
    @abstractmethod
    def metadata(self) -> MissionMetadata:
        """Return this plugin's static identity."""

    @property
    @abstractmethod
    def state(self) -> MissionState:
        """Return the plugin's current lifecycle state."""

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> bool:
        """Validate ``config`` and establish internal mission state."""

    @abstractmethod
    def start(self) -> bool:
        """Begin mission execution. Return True if started successfully."""

    @abstractmethod
    def pause(self) -> bool:
        """Pause an in-progress mission. Return True if paused successfully."""

    @abstractmethod
    def resume(self) -> bool:
        """Resume a paused mission. Return True if resumed successfully."""

    @abstractmethod
    def abort(self, reason: str) -> None:
        """Abort the mission immediately and leave the system in a safe state."""

    @abstractmethod
    def shutdown(self) -> None:
        """Release mission resources and leave the system in a safe state."""

    @abstractmethod
    def diagnostics(self) -> dict[str, Any]:
        """Return current mission state, last event, and error/fault counts."""
