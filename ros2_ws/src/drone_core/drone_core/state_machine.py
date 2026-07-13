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
CoreStateMachine implements IStateMachine against the canonical transition table.

Owned by drone_interfaces. This class owns only behavior (single-threaded
transition application, observer notification, history); it never
redefines which transitions are legal.
"""

from __future__ import annotations

from drone_interfaces.exceptions import StateTransitionError
from drone_interfaces.state_machine import (
    IStateMachine,
    StateObserver,
    StateTransition,
    SystemState,
    VALID_TRANSITIONS,
)


class CoreStateMachine(IStateMachine):
    """Concrete platform state machine, starting in SystemState.BOOTING."""

    def __init__(self) -> None:
        self._current = SystemState.BOOTING
        self._observers: list[StateObserver] = []
        self._history: list[StateTransition] = []

    @property
    def current_state(self) -> SystemState:
        return self._current

    def can_transition(self, target: SystemState) -> bool:
        return target in VALID_TRANSITIONS[self._current]

    def transition(self, target: SystemState, reason: str) -> StateTransition:
        if not self.can_transition(target):
            raise StateTransitionError(
                f'{self._current.name} -> {target.name} is not a legal transition',
            )
        record = StateTransition(from_state=self._current, to_state=target, reason=reason)
        self._current = target
        self._history.append(record)
        for observer in self._observers:
            observer(record)
        return record

    def register_observer(self, observer: StateObserver) -> None:
        self._observers.append(observer)

    def history(self) -> tuple[StateTransition, ...]:
        return tuple(self._history)
