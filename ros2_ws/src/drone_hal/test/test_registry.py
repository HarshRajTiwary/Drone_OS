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

"""Unit tests for HardwareRegistry."""

from _fakes import FakeDriver
from drone_hal.device import BusType, DeviceDescriptor
from drone_hal.exceptions import DeviceAlreadyRegisteredError, DeviceNotFoundError
from drone_hal.registry import HardwareRegistry
import pytest


def _descriptor(device_id: str = 'rf0') -> DeviceDescriptor:
    return DeviceDescriptor(
        device_id=device_id, device_type='rangefinder', bus=BusType.UART,
        address='/dev/ttyAMA0', driver_class='pkg.mod:Cls',
    )


def test_register_and_list_devices():
    registry = HardwareRegistry()
    descriptor = _descriptor()
    registry.register(descriptor, lambda: FakeDriver(descriptor))
    assert registry.list_devices() == [descriptor]


def test_duplicate_registration_raises():
    registry = HardwareRegistry()
    descriptor = _descriptor()
    registry.register(descriptor, lambda: FakeDriver(descriptor))
    with pytest.raises(DeviceAlreadyRegisteredError):
        registry.register(descriptor, lambda: FakeDriver(descriptor))


def test_get_unregistered_device_raises():
    registry = HardwareRegistry()
    with pytest.raises(DeviceNotFoundError):
        registry.get('does_not_exist')


def test_get_lazily_instantiates_and_caches():
    registry = HardwareRegistry()
    descriptor = _descriptor()
    build_count = 0

    def factory():
        nonlocal build_count
        build_count += 1
        return FakeDriver(descriptor)

    registry.register(descriptor, factory)
    assert registry.instantiated_devices() == []

    first = registry.get(descriptor.device_id)
    second = registry.get(descriptor.device_id)
    assert first is second
    assert build_count == 1
    assert registry.instantiated_devices() == [descriptor.device_id]


def test_unregister_discards_instance():
    registry = HardwareRegistry()
    descriptor = _descriptor()
    registry.register(descriptor, lambda: FakeDriver(descriptor))
    registry.get(descriptor.device_id)
    registry.unregister(descriptor.device_id)
    assert registry.list_devices() == []
    with pytest.raises(DeviceNotFoundError):
        registry.get(descriptor.device_id)
