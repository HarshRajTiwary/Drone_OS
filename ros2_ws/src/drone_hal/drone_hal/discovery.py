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
Generic device discovery: bus-level presence checks only.

drone_hal cannot know how to speak to a specific chip (that is each
driver package's job), so discovery here answers only "does the
configured bus/address exist on this host" (e.g. does
``/dev/spidev0.0`` exist). Protocol-level probing (e.g. reading a TFMini-S
frame header) belongs in that device's own driver, exercised during
LifecycleComponent.on_configure().
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import os

from drone_hal.device import BusType, DeviceConnectivity, DeviceDescriptor

#: Bus types whose address is a filesystem device node we can os.path.exists() check.
_FILESYSTEM_BUSES = frozenset({BusType.UART, BusType.SPI, BusType.I2C, BusType.CSI})


class IDeviceDiscovery(ABC):
    """Contract for probing bus-level presence of configured devices."""

    @abstractmethod
    def scan(
        self, descriptors: list[DeviceDescriptor],
    ) -> dict[str, DeviceConnectivity]:
        """Return each descriptor's device_id mapped to its DeviceConnectivity."""


class DeviceDiscovery(IDeviceDiscovery):
    """Filesystem-presence-based discovery for UART/SPI/I2C/CSI device nodes."""

    def scan(
        self, descriptors: list[DeviceDescriptor],
    ) -> dict[str, DeviceConnectivity]:
        results: dict[str, DeviceConnectivity] = {}
        for descriptor in descriptors:
            results[descriptor.device_id] = self._probe(descriptor)
        return results

    def _probe(self, descriptor: DeviceDescriptor) -> DeviceConnectivity:
        if descriptor.bus not in _FILESYSTEM_BUSES:
            return DeviceConnectivity.UNKNOWN
        return (
            DeviceConnectivity.PRESENT
            if os.path.exists(descriptor.address)
            else DeviceConnectivity.MISSING
        )
