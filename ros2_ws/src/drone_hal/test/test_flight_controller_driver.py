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

"""Unit tests for the flight controller telemetry driver contract."""

from drone_hal.flight_controller_driver import (
    BatteryStatus,
    IFlightControllerDriver,
    RCStatus,
    VehicleStatus,
)
import pytest


def test_cannot_instantiate_abstract_flight_controller_driver():
    with pytest.raises(TypeError):
        IFlightControllerDriver()


def test_flight_controller_driver_has_no_command_methods():
    forbidden = {'arm', 'disarm', 'takeoff', 'land', 'set_mode', 'send_command'}
    declared = set(dir(IFlightControllerDriver))
    assert forbidden.isdisjoint(declared)


def test_vehicle_status_fields():
    status = VehicleStatus(armed=False, mode='STABILIZE', system_status='STANDBY', timestamp=0.0)
    assert status.armed is False
    assert status.mode == 'STABILIZE'


def test_battery_status_fields():
    battery = BatteryStatus(
        voltage_v=12.4, current_a=3.1, remaining_percent=87.0, timestamp=0.0,
    )
    assert battery.remaining_percent == 87.0


def test_rc_status_fields():
    rc = RCStatus(connected=True, rssi_percent=90.0, channel_count=8, timestamp=0.0)
    assert rc.connected is True
    assert rc.channel_count == 8
