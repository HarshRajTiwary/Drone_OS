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
Optical flow driver contract, per docs/interfaces/optical_flow_interface.md.

drone_optical_flow (Phase 2 package 5) implements IOpticalFlowDriver
against the Holybro PMW3901 over SPI. Motion fusion and navigation use of
these measurements are out of scope here and belong to Navigation, a
later phase.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from time import time

from drone_hal.driver import IHardwareDriver


@dataclass(frozen=True)
class FlowMeasurement:
    """A single optical flow sample."""

    delta_x: float
    delta_y: float
    quality: float
    sequence: int
    timestamp: float = field(default_factory=time)


class IOpticalFlowDriver(IHardwareDriver):
    """Contract for acquiring motion estimates from an optical flow sensor."""

    @abstractmethod
    def read_flow(self) -> FlowMeasurement:
        """
        Acquire and return the next optical flow measurement.

        Raises HealthCheckError if the device cannot produce a
        measurement (not available, communication failure, or timeout).
        """
