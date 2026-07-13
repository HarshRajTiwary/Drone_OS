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
Platform state machine contract.

Defines the canonical DroneOS system states and the single source of truth
for which transitions are legal. drone_core's State Manager implements
IStateMachine against this table; no other package may redefine it.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import auto, Enum
from time import time


class SystemState(Enum):
    """Top-level DroneOS runtime state."""

    BOOTING = auto()
    INITIALIZING = auto()
    READY = auto()
    MISSION_RUNNING = auto()
    PAUSED = auto()
    ERROR = auto()
    SHUTDOWN = auto()


#: Canonical legal-transition table. SHUTDOWN is terminal.
VALID_TRANSITIONS: dict[SystemState, frozenset[SystemState]] = {
    SystemState.BOOTING: frozenset({SystemState.INITIALIZING, SystemState.ERROR}),
    SystemState.INITIALIZING: frozenset({SystemState.READY, SystemState.ERROR}),
    SystemState.READY: frozenset({
        SystemState.MISSION_RUNNING, SystemState.SHUTDOWN, SystemState.ERROR,
    }),
    SystemState.MISSION_RUNNING: frozenset({
        SystemState.PAUSED, SystemState.READY, SystemState.ERROR, SystemState.SHUTDOWN,
    }),
    SystemState.PAUSED: frozenset({
        SystemState.MISSION_RUNNING, SystemState.READY,
        SystemState.ERROR, SystemState.SHUTDOWN,
    }),
    SystemState.ERROR: frozenset({SystemState.INITIALIZING, SystemState.SHUTDOWN}),
    SystemState.SHUTDOWN: frozenset(),
}


@dataclass(frozen=True)
class StateTransition:
    """Record of a single state transition."""

    from_state: SystemState
    to_state: SystemState
    reason: str
    timestamp: float = field(default_factory=time)


StateObserver = Callable[[StateTransition], None]


class IStateMachine(ABC):
    """Contract for the platform-wide state machine."""

    @property
    @abstractmethod
    def current_state(self) -> SystemState:
        """Return the current system state."""

    @abstractmethod
    def can_transition(self, target: SystemState) -> bool:
        """Return True if transitioning to ``target`` is currently legal."""

    @abstractmethod
    def transition(self, target: SystemState, reason: str) -> StateTransition:
        """
        Attempt a transition to ``target``.

        Raises StateTransitionError if the transition is not legal.
        """

    @abstractmethod
    def register_observer(self, observer: StateObserver) -> None:
        """Register a callback invoked on every successful transition."""

    @abstractmethod
    def history(self) -> tuple[StateTransition, ...]:
        """Return the ordered history of transitions since boot."""
