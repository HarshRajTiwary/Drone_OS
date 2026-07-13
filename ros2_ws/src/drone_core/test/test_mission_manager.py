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

"""Unit tests for CoreMissionRegistry."""

from drone_core.mission_manager import CoreMissionRegistry
from drone_interfaces.exceptions import MissionError
from drone_interfaces.lifecycle import LifecycleState
from drone_interfaces.mission import IMissionPlugin, MissionMetadata, MissionState
import pytest


class _FakeMission(IMissionPlugin):
    def __init__(self, name: str = 'fake') -> None:
        self._metadata = MissionMetadata(name=name, version='0.1.0', description='d')
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


def test_register_and_discover():
    registry = CoreMissionRegistry()
    registry.register(_FakeMission, MissionMetadata(name='fake', version='0.1.0', description='d'))
    assert [m.name for m in registry.discover()] == ['fake']


def test_duplicate_registration_raises():
    registry = CoreMissionRegistry()
    metadata = MissionMetadata(name='fake', version='0.1.0', description='d')
    registry.register(_FakeMission, metadata)
    with pytest.raises(MissionError):
        registry.register(_FakeMission, metadata)


def test_activate_unknown_mission_raises():
    registry = CoreMissionRegistry()
    with pytest.raises(MissionError):
        registry.activate('nope', {})


def test_activate_then_deactivate_round_trip():
    registry = CoreMissionRegistry()
    registry.register(_FakeMission, MissionMetadata(name='fake', version='0.1.0', description='d'))
    assert registry.activate('fake', {}) is True
    assert registry.active_mission() is not None
    assert registry.mission_state('fake') is MissionState.RUNNING
    assert registry.deactivate('fake') is True
    assert registry.active_mission() is None


def test_second_concurrent_activation_raises():
    registry = CoreMissionRegistry()
    registry.register(_FakeMission, MissionMetadata(name='a', version='0.1.0', description='d'))
    registry.register(
        lambda: _FakeMission('b'), MissionMetadata(name='b', version='0.1.0', description='d'),
    )
    registry.activate('a', {})
    with pytest.raises(MissionError):
        registry.activate('b', {})


def test_lifecycle_walk():
    registry = CoreMissionRegistry()
    assert registry.on_configure() is True
    assert registry.lifecycle_state is LifecycleState.INACTIVE
    assert registry.on_activate() is True
    assert registry.lifecycle_state is LifecycleState.ACTIVE
    assert registry.on_deactivate() is True
    assert registry.on_cleanup() is True
    assert registry.on_shutdown() is True
    assert registry.lifecycle_state is LifecycleState.FINALIZED


def test_shutdown_deactivates_active_mission():
    registry = CoreMissionRegistry()
    registry.register(_FakeMission, MissionMetadata(name='fake', version='0.1.0', description='d'))
    registry.activate('fake', {})
    registry.on_shutdown()
    assert registry.active_mission() is None
