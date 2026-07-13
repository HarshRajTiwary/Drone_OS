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

"""
Flight controller telemetry driver contract.

Per docs/interfaces/flight_controller_interface.md. drone_fc (Phase 2
package 3) implements IFlightControllerDriver against the
Pixhawk 2.4.8 / ArduPilot over MAVLink. This contract is read-only
telemetry and connection management: it deliberately has no arm, takeoff,
mode-change, or command-dispatch methods. Those belong to Flight Core, a
later phase.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from time import time

from drone_hal.driver import IHardwareDriver


@dataclass(frozen=True)
class VehicleStatus:
    """Autopilot-reported vehicle state, read-only."""

    armed: bool
    mode: str
    system_status: str
    timestamp: float = field(default_factory=time)


@dataclass(frozen=True)
class BatteryStatus:
    """Battery telemetry reported by the flight controller."""

    voltage_v: float
    current_a: float
    remaining_percent: float
    timestamp: float = field(default_factory=time)


@dataclass(frozen=True)
class RCStatus:
    """RC receiver status as reported through the flight controller."""

    connected: bool
    rssi_percent: float
    channel_count: int
    timestamp: float = field(default_factory=time)


class IFlightControllerDriver(IHardwareDriver):
    """Read-only contract for Pixhawk/ArduPilot connection and telemetry."""

    @abstractmethod
    def heartbeat_age_seconds(self) -> float:
        """Return seconds since the last received MAVLink heartbeat."""

    @abstractmethod
    def get_vehicle_status(self) -> VehicleStatus:
        """Return the current vehicle armed/mode/system-status snapshot."""

    @abstractmethod
    def get_battery_status(self) -> BatteryStatus:
        """Return the current battery telemetry snapshot."""

    @abstractmethod
    def get_rc_status(self) -> RCStatus:
        """Return the current RC receiver status snapshot."""
