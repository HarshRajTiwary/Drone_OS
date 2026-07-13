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

"""Unit tests for CoreStateMachine."""

from drone_core.state_machine import CoreStateMachine
from drone_interfaces.exceptions import StateTransitionError
from drone_interfaces.state_machine import SystemState
import pytest


def test_starts_in_booting():
    assert CoreStateMachine().current_state is SystemState.BOOTING


def test_legal_transition_updates_current_state():
    machine = CoreStateMachine()
    machine.transition(SystemState.INITIALIZING, 'starting')
    assert machine.current_state is SystemState.INITIALIZING


def test_illegal_transition_raises():
    machine = CoreStateMachine()
    with pytest.raises(StateTransitionError):
        machine.transition(SystemState.MISSION_RUNNING, 'skip ahead')


def test_history_records_every_transition():
    machine = CoreStateMachine()
    machine.transition(SystemState.INITIALIZING, 'a')
    machine.transition(SystemState.READY, 'b')
    assert [t.to_state for t in machine.history()] == [
        SystemState.INITIALIZING, SystemState.READY,
    ]


def test_observers_are_notified_on_transition():
    machine = CoreStateMachine()
    seen = []
    machine.register_observer(seen.append)
    machine.transition(SystemState.INITIALIZING, 'a')
    assert len(seen) == 1
    assert seen[0].to_state is SystemState.INITIALIZING
