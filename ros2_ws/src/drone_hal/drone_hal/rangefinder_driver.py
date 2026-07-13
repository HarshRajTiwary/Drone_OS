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
Rangefinder driver contract, per docs/interfaces/rangefinder_interface.md.

drone_rangefinder (Phase 2 package 4) implements IRangefinderDriver against
the TFMini-S over UART. Filtering and calibration are the implementing
package's responsibility; this module defines only the acquisition
contract and the measurement shape.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from time import time

from drone_hal.driver import IHardwareDriver


@dataclass(frozen=True)
class DistanceMeasurement:
    """A single distance sample with validity and signal-quality metadata."""

    distance_m: float
    valid: bool
    signal_strength: float
    sequence: int
    timestamp: float = field(default_factory=time)


class IRangefinderDriver(IHardwareDriver):
    """Contract for acquiring distance measurements from a rangefinder."""

    @abstractmethod
    def read_distance(self) -> DistanceMeasurement:
        """
        Acquire and return the next distance measurement.

        Raises HealthCheckError if the device cannot produce a
        measurement (not available, communication failure, or timeout).
        """
