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

"""Unit tests for the device descriptor and connectivity model."""

from drone_hal.device import BusType, DeviceConnectivity, DeviceDescriptor
import pytest


def test_bus_type_covers_target_hardware_buses():
    assert {b.name for b in BusType} == {'UART', 'SPI', 'I2C', 'CSI', 'USB', 'GPIO'}


def test_device_connectivity_has_expected_members():
    assert {c.name for c in DeviceConnectivity} == {
        'UNKNOWN', 'PRESENT', 'MISSING', 'DISCONNECTED',
    }


def test_device_descriptor_metadata_defaults_to_empty_dict():
    descriptor = DeviceDescriptor(
        device_id='cam0', device_type='camera', bus=BusType.CSI,
        address='/dev/video0', driver_class='pkg.mod:Cls',
    )
    assert descriptor.metadata == {}


def test_device_descriptor_is_frozen():
    descriptor = DeviceDescriptor(
        device_id='cam0', device_type='camera', bus=BusType.CSI,
        address='/dev/video0', driver_class='pkg.mod:Cls',
    )
    with pytest.raises(AttributeError):
        descriptor.device_id = 'other'
