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
Camera driver contract, per docs/interfaces/camera_interface.md.

drone_camera (Phase 2 package 2) implements ICameraDriver against the Pi
Camera Module / libcamera. This module defines the contract only: no
image processing, no capture implementation.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from time import time

from drone_hal.driver import IHardwareDriver


@dataclass(frozen=True)
class Frame:
    """A single captured image and its acquisition metadata."""

    data: bytes
    width: int
    height: int
    encoding: str
    sequence: int
    timestamp: float = field(default_factory=time)


class ICameraDriver(IHardwareDriver):
    """Contract for acquiring frames from a camera device."""

    @abstractmethod
    def capture(self) -> Frame:
        """
        Acquire and return the next available frame.

        Raises HealthCheckError if the device cannot produce a frame
        (not available, capture failure, or timeout).
        """

    @abstractmethod
    def get_calibration(self) -> dict[str, float] | None:
        """Return calibration parameters, or None if calibration is missing."""
