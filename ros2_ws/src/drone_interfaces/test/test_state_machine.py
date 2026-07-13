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

"""Unit tests for the SystemState contract and its canonical transition table."""

from drone_interfaces.state_machine import (
    IStateMachine,
    StateTransition,
    SystemState,
    VALID_TRANSITIONS,
)
import pytest


def test_system_state_enum_matches_required_states():
    assert {s.name for s in SystemState} == {
        'BOOTING', 'INITIALIZING', 'READY', 'MISSION_RUNNING',
        'PAUSED', 'ERROR', 'SHUTDOWN',
    }


def test_every_state_has_a_transition_table_entry():
    assert set(VALID_TRANSITIONS.keys()) == set(SystemState)


def test_shutdown_is_terminal():
    assert VALID_TRANSITIONS[SystemState.SHUTDOWN] == frozenset()


def test_booting_leads_to_initializing():
    assert SystemState.INITIALIZING in VALID_TRANSITIONS[SystemState.BOOTING]


def test_ready_reaches_mission_running_and_shutdown():
    transitions = VALID_TRANSITIONS[SystemState.READY]
    assert SystemState.MISSION_RUNNING in transitions
    assert SystemState.SHUTDOWN in transitions


def test_every_non_terminal_state_can_reach_shutdown_directly_or_transitively():
    # Fail-safe requirement: no state should be able to strand the platform
    # without a path to SHUTDOWN.
    for state in SystemState:
        if state is SystemState.SHUTDOWN:
            continue
        visited = {state}
        frontier = [state]
        reachable = False
        while frontier:
            current = frontier.pop()
            for nxt in VALID_TRANSITIONS[current]:
                if nxt is SystemState.SHUTDOWN:
                    reachable = True
                    break
                if nxt not in visited:
                    visited.add(nxt)
                    frontier.append(nxt)
            if reachable:
                break
        assert reachable, f'{state} cannot reach SHUTDOWN'


def test_cannot_instantiate_abstract_state_machine():
    with pytest.raises(TypeError):
        IStateMachine()


def test_state_transition_dataclass_is_frozen():
    transition = StateTransition(
        from_state=SystemState.BOOTING,
        to_state=SystemState.INITIALIZING,
        reason='boot sequence complete',
    )
    assert transition.from_state is SystemState.BOOTING
    assert transition.to_state is SystemState.INITIALIZING
    with pytest.raises(AttributeError):
        transition.reason = 'mutated'
