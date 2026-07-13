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

"""Unit tests for the IHardwareDriver contract, exercised via FakeDriver."""

from _fakes import FakeDriver
from drone_hal.device import BusType, DeviceConnectivity, DeviceDescriptor
from drone_hal.driver import IHardwareDriver
from drone_interfaces.health import HealthStatus
from drone_interfaces.lifecycle import LifecycleState
import pytest


def _descriptor() -> DeviceDescriptor:
    return DeviceDescriptor(
        device_id='rf0', device_type='rangefinder', bus=BusType.UART,
        address='/dev/ttyAMA0', driver_class='pkg.mod:Cls',
    )


def test_cannot_instantiate_abstract_driver():
    with pytest.raises(TypeError):
        IHardwareDriver()


def test_fake_driver_walks_full_lifecycle():
    driver = FakeDriver(_descriptor())
    assert driver.lifecycle_state is LifecycleState.UNCONFIGURED

    assert driver.on_configure() is True
    assert driver.lifecycle_state is LifecycleState.INACTIVE

    assert driver.on_activate() is True
    assert driver.lifecycle_state is LifecycleState.ACTIVE

    assert driver.on_deactivate() is True
    assert driver.on_cleanup() is True
    assert driver.on_shutdown() is True
    assert driver.lifecycle_state is LifecycleState.FINALIZED


def test_fake_driver_reports_health():
    driver = FakeDriver(_descriptor())
    report = driver.check_health()
    assert report.status is HealthStatus.OK
    assert report.component == 'rf0'


def test_fake_driver_reconnect_restores_presence():
    driver = FakeDriver(_descriptor())
    driver._connectivity = DeviceConnectivity.DISCONNECTED
    assert driver.reconnect() is True
    assert driver.connectivity is DeviceConnectivity.PRESENT
