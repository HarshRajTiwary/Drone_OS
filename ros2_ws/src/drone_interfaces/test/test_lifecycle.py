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

"""Unit tests for the LifecycleComponent contract."""

from drone_interfaces.lifecycle import LifecycleComponent, LifecycleState
import pytest


class _FakeComponent(LifecycleComponent):
    """Minimal concrete implementation used to exercise the ABC contract."""

    def __init__(self) -> None:
        self._state = LifecycleState.UNCONFIGURED

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    def on_configure(self) -> bool:
        self._state = LifecycleState.INACTIVE
        return True

    def on_activate(self) -> bool:
        self._state = LifecycleState.ACTIVE
        return True

    def on_deactivate(self) -> bool:
        self._state = LifecycleState.INACTIVE
        return True

    def on_cleanup(self) -> bool:
        self._state = LifecycleState.UNCONFIGURED
        return True

    def on_shutdown(self) -> bool:
        self._state = LifecycleState.FINALIZED
        return True

    def on_error(self, error: Exception) -> bool:
        return False


def test_cannot_instantiate_abstract_lifecycle_component():
    with pytest.raises(TypeError):
        LifecycleComponent()


def test_fake_component_transitions_through_full_lifecycle():
    component = _FakeComponent()
    assert component.lifecycle_state is LifecycleState.UNCONFIGURED

    assert component.on_configure() is True
    assert component.lifecycle_state is LifecycleState.INACTIVE

    assert component.on_activate() is True
    assert component.lifecycle_state is LifecycleState.ACTIVE

    assert component.on_deactivate() is True
    assert component.lifecycle_state is LifecycleState.INACTIVE

    assert component.on_cleanup() is True
    assert component.lifecycle_state is LifecycleState.UNCONFIGURED

    assert component.on_shutdown() is True
    assert component.lifecycle_state is LifecycleState.FINALIZED


def test_lifecycle_state_enum_has_expected_members():
    assert {s.name for s in LifecycleState} == {
        'UNCONFIGURED', 'INACTIVE', 'ACTIVE', 'FINALIZED',
    }
