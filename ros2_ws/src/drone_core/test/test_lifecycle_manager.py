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

"""Unit tests for LifecycleManager's fan-out and fault isolation."""

from drone_core.lifecycle_manager import LifecycleManager
from drone_interfaces.lifecycle import LifecycleComponent, LifecycleState


class _FakeComponent(LifecycleComponent):
    def __init__(self, fail_on: str | None = None) -> None:
        self._state = LifecycleState.UNCONFIGURED
        self._fail_on = fail_on
        self.calls: list[str] = []

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    def _run(self, name, next_state):
        self.calls.append(name)
        if self._fail_on == name:
            raise RuntimeError(f'{name} failed')
        self._state = next_state
        return True

    def on_configure(self):
        return self._run('on_configure', LifecycleState.INACTIVE)

    def on_activate(self):
        return self._run('on_activate', LifecycleState.ACTIVE)

    def on_deactivate(self):
        return self._run('on_deactivate', LifecycleState.INACTIVE)

    def on_cleanup(self):
        return self._run('on_cleanup', LifecycleState.UNCONFIGURED)

    def on_shutdown(self):
        return self._run('on_shutdown', LifecycleState.FINALIZED)

    def on_error(self, error):
        self.calls.append('on_error')
        return False


def test_configure_activate_shutdown_across_two_components():
    a, b = _FakeComponent(), _FakeComponent()
    manager = LifecycleManager({'a': a, 'b': b})

    assert manager.on_configure() is True
    assert manager.lifecycle_state is LifecycleState.INACTIVE
    assert manager.on_activate() is True
    assert manager.lifecycle_state is LifecycleState.ACTIVE
    assert manager.on_shutdown() is True
    assert manager.lifecycle_state is LifecycleState.FINALIZED


def test_one_component_failure_does_not_block_the_other():
    healthy = _FakeComponent()
    faulty = _FakeComponent(fail_on='on_activate')
    manager = LifecycleManager({'healthy': healthy, 'faulty': faulty})

    manager.on_configure()
    overall = manager.on_activate()

    assert overall is False
    assert healthy.lifecycle_state is LifecycleState.ACTIVE
    assert faulty.lifecycle_state is LifecycleState.INACTIVE
    assert 'on_error' in faulty.calls


def test_component_accessor_returns_named_component():
    a = _FakeComponent()
    manager = LifecycleManager({'a': a})
    assert manager.component('a') is a
