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
Generic hardware driver contract.

Every concrete driver (camera, flight controller, rangefinder, optical
flow, GPIO, ...) implements IHardwareDriver. It composes two Phase 1
contracts rather than reinventing them: LifecycleComponent for
initialize/configure/activate/deactivate/cleanup/shutdown, and
IHealthCheckable for health reporting. This is deliberate reuse, not
new state machinery: drone_hal only adds what those contracts do not
cover, which is physical presence (see device.py) and reconnection.
"""

from __future__ import annotations

from abc import abstractmethod

from drone_hal.device import DeviceConnectivity, DeviceDescriptor
from drone_interfaces.health import IHealthCheckable
from drone_interfaces.lifecycle import LifecycleComponent


class IHardwareDriver(LifecycleComponent, IHealthCheckable):
    """Contract every HAL device driver must satisfy."""

    @property
    @abstractmethod
    def descriptor(self) -> DeviceDescriptor:
        """Return this driver's static device identity."""

    @property
    @abstractmethod
    def connectivity(self) -> DeviceConnectivity:
        """Return whether the physical device is currently present."""

    @abstractmethod
    def reconnect(self) -> bool:
        """
        Attempt to re-establish communication with the device.

        Returns True if the device is reachable again, without changing
        the driver's LifecycleState (a reconnect does not re-run
        configuration).
        """
