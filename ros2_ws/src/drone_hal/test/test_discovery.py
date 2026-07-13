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

"""Unit tests for DeviceDiscovery (bus-presence checks)."""

from drone_hal.device import BusType, DeviceConnectivity, DeviceDescriptor
from drone_hal.discovery import DeviceDiscovery


def test_scan_reports_present_for_existing_path(tmp_path):
    existing = tmp_path / 'ttyFAKE'
    existing.write_text('')
    descriptor = DeviceDescriptor(
        device_id='rf0', device_type='rangefinder', bus=BusType.UART,
        address=str(existing), driver_class='pkg.mod:Cls',
    )
    results = DeviceDiscovery().scan([descriptor])
    assert results['rf0'] is DeviceConnectivity.PRESENT


def test_scan_reports_missing_for_absent_path(tmp_path):
    descriptor = DeviceDescriptor(
        device_id='rf0', device_type='rangefinder', bus=BusType.UART,
        address=str(tmp_path / 'does_not_exist'), driver_class='pkg.mod:Cls',
    )
    results = DeviceDiscovery().scan([descriptor])
    assert results['rf0'] is DeviceConnectivity.MISSING


def test_scan_reports_unknown_for_non_filesystem_bus():
    descriptor = DeviceDescriptor(
        device_id='fc0', device_type='flight_controller', bus=BusType.USB,
        address='vid:pid', driver_class='pkg.mod:Cls',
    )
    results = DeviceDiscovery().scan([descriptor])
    assert results['fc0'] is DeviceConnectivity.UNKNOWN


def test_scan_handles_multiple_descriptors():
    descriptors = [
        DeviceDescriptor(
            device_id=f'dev{i}', device_type='rangefinder', bus=BusType.UART,
            address=f'/nonexistent/{i}', driver_class='pkg.mod:Cls',
        )
        for i in range(3)
    ]
    results = DeviceDiscovery().scan(descriptors)
    assert set(results.keys()) == {'dev0', 'dev1', 'dev2'}
