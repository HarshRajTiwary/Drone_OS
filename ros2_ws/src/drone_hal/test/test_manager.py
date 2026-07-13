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

"""Integration tests for HardwareManager's lifecycle fan-out and diagnostics."""

from _fakes import FakeDriver
from drone_hal.device import BusType, DeviceDescriptor
from drone_hal.discovery import DeviceDiscovery
from drone_hal.loader import DriverLoader
from drone_hal.manager import HardwareManager
from drone_hal.registry import HardwareRegistry
from drone_interfaces.diagnostics import DiagnosticLevel
from drone_interfaces.lifecycle import LifecycleState


def _descriptor(device_id: str) -> DeviceDescriptor:
    return DeviceDescriptor(
        device_id=device_id, device_type='rangefinder', bus=BusType.UART,
        address='/dev/null', driver_class='_fakes:FakeDriver',
    )


def _manager(*device_ids: str) -> HardwareManager:
    return HardwareManager(
        registry=HardwareRegistry(),
        loader=DriverLoader(),
        discovery=DeviceDiscovery(),
        descriptors=[_descriptor(d) for d in device_ids],
    )


def test_manager_is_a_lifecycle_component():
    manager = _manager('rf0')
    assert manager.lifecycle_state is LifecycleState.UNCONFIGURED


def test_full_lifecycle_walk_across_two_devices():
    manager = _manager('rf0', 'rf1')

    assert manager.on_configure() is True
    assert manager.lifecycle_state is LifecycleState.INACTIVE
    assert {d.device_id for d in manager.registry.list_devices()} == {'rf0', 'rf1'}

    assert manager.on_activate() is True
    assert manager.lifecycle_state is LifecycleState.ACTIVE

    assert manager.on_deactivate() is True
    assert manager.on_cleanup() is True
    assert manager.lifecycle_state is LifecycleState.UNCONFIGURED


def test_shutdown_reaches_finalized():
    manager = _manager('rf0')
    manager.on_configure()
    manager.on_activate()
    assert manager.on_shutdown() is True
    assert manager.lifecycle_state is LifecycleState.FINALIZED


def test_collect_diagnostics_reflects_fake_driver_health():
    manager = _manager('rf0')
    manager.on_configure()
    manager.on_activate()
    reports = manager.collect_diagnostics()
    assert len(reports) == 1
    assert reports[0].name == 'rf0'
    assert reports[0].level == DiagnosticLevel.OK
    assert reports[0].items[0].key == 'reads'


def test_collect_diagnostics_empty_before_any_device_instantiated():
    manager = _manager('rf0')
    assert manager.collect_diagnostics() == []


def test_rediscover_returns_connectivity_without_changing_lifecycle_state():
    manager = _manager('rf0')
    manager.on_configure()
    manager.on_activate()
    connectivity = manager.rediscover()
    assert 'rf0' in connectivity
    assert manager.lifecycle_state is LifecycleState.ACTIVE


def test_one_device_failure_does_not_block_its_siblings():
    healthy = _descriptor('rf_healthy')
    faulty = _descriptor('rf_faulty')
    manager = HardwareManager(
        registry=HardwareRegistry(),
        loader=DriverLoader(),
        discovery=DeviceDiscovery(),
        descriptors=[healthy, faulty],
    )
    manager.on_configure()

    # Swap the faulty device's registry entry for one that fails on
    # activation, so on_activate()'s fan-out has a real fault to isolate.
    manager.registry.unregister('rf_faulty')
    manager.registry.register(
        faulty, lambda: FakeDriver(faulty, fail_on='on_activate'),
    )

    overall_success = manager.on_activate()
    assert overall_success is False

    healthy_driver = manager.registry.get('rf_healthy')
    faulty_driver = manager.registry.get('rf_faulty')
    assert healthy_driver.lifecycle_state is LifecycleState.ACTIVE
    assert faulty_driver.lifecycle_state is LifecycleState.UNCONFIGURED
    assert 'on_error' in faulty_driver.calls
