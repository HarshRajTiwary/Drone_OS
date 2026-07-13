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

"""Unit tests for the mission plugin and mission registry contracts."""

from drone_interfaces.exceptions import MissionError
from drone_interfaces.mission import IMissionPlugin, MissionMetadata, MissionState
from drone_interfaces.mission_registry import IMissionRegistry
import pytest


class _FakeMissionPlugin(IMissionPlugin):
    def __init__(self, name: str = 'fake_mission') -> None:
        self._metadata = MissionMetadata(name=name, version='0.1.0', description='test double')
        self._state = MissionState.UNINITIALIZED

    @property
    def metadata(self) -> MissionMetadata:
        return self._metadata

    @property
    def state(self) -> MissionState:
        return self._state

    def initialize(self, config):
        self._state = MissionState.INITIALIZED
        return True

    def start(self):
        self._state = MissionState.RUNNING
        return True

    def pause(self):
        self._state = MissionState.PAUSED
        return True

    def resume(self):
        self._state = MissionState.RUNNING
        return True

    def abort(self, reason):
        self._state = MissionState.ABORTED

    def shutdown(self):
        self._state = MissionState.COMPLETED

    def diagnostics(self):
        return {'state': self._state.name}


class _FakeRegistry(IMissionRegistry):
    def __init__(self) -> None:
        self._factories: dict[str, tuple] = {}
        self._active: IMissionPlugin | None = None

    def register(self, factory, metadata):
        if metadata.name in self._factories:
            raise MissionError(f'{metadata.name} already registered')
        self._factories[metadata.name] = (factory, metadata)

    def discover(self):
        return [meta for _, meta in self._factories.values()]

    def activate(self, name, config):
        if name not in self._factories:
            raise MissionError(f'unknown mission {name}')
        if self._active is not None:
            raise MissionError('another mission is already active')
        factory, _ = self._factories[name]
        plugin = factory()
        plugin.initialize(config)
        plugin.start()
        self._active = plugin
        return True

    def deactivate(self, name):
        if self._active is None or self._active.metadata.name != name:
            return False
        self._active.shutdown()
        self._active = None
        return True

    def active_mission(self):
        return self._active

    def mission_state(self, name):
        if self._active is not None and self._active.metadata.name == name:
            return self._active.state
        return MissionState.UNINITIALIZED


def test_cannot_instantiate_abstract_mission_plugin():
    with pytest.raises(TypeError):
        IMissionPlugin()


def test_cannot_instantiate_abstract_mission_registry():
    with pytest.raises(TypeError):
        IMissionRegistry()


def test_mission_state_enum_covers_full_lifecycle():
    assert {s.name for s in MissionState} == {
        'UNINITIALIZED', 'INITIALIZED', 'RUNNING', 'PAUSED',
        'COMPLETED', 'ABORTED', 'FAILED',
    }


def test_registry_registers_and_discovers_plugin():
    registry = _FakeRegistry()
    registry.register(_FakeMissionPlugin, MissionMetadata(
        name='fake_mission', version='0.1.0', description='test double',
    ))
    assert [m.name for m in registry.discover()] == ['fake_mission']


def test_registry_rejects_duplicate_registration():
    registry = _FakeRegistry()
    metadata = MissionMetadata(name='fake_mission', version='0.1.0', description='d')
    registry.register(_FakeMissionPlugin, metadata)
    with pytest.raises(MissionError):
        registry.register(_FakeMissionPlugin, metadata)


def test_registry_activate_then_deactivate_round_trip():
    registry = _FakeRegistry()
    registry.register(_FakeMissionPlugin, MissionMetadata(
        name='fake_mission', version='0.1.0', description='d',
    ))
    assert registry.activate('fake_mission', {}) is True
    assert registry.active_mission() is not None
    assert registry.mission_state('fake_mission') == MissionState.RUNNING

    assert registry.deactivate('fake_mission') is True
    assert registry.active_mission() is None


def test_registry_rejects_activating_unknown_mission():
    registry = _FakeRegistry()
    with pytest.raises(MissionError):
        registry.activate('does_not_exist', {})


def test_registry_rejects_second_concurrent_activation():
    registry = _FakeRegistry()
    registry.register(_FakeMissionPlugin, MissionMetadata(
        name='mission_a', version='0.1.0', description='d',
    ))
    registry.register(
        lambda: _FakeMissionPlugin('mission_b'),
        MissionMetadata(name='mission_b', version='0.1.0', description='d'),
    )
    registry.activate('mission_a', {})
    with pytest.raises(MissionError):
        registry.activate('mission_b', {})
