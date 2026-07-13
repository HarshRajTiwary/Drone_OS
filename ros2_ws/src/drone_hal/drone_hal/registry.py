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
Hardware device registry: tracks which drivers exist and their descriptors.

The registry stores driver *factories*, not instances, until a caller asks
for one. This mirrors IMissionRegistry's pattern from drone_interfaces
(Phase 1) applied to hardware: registration/discovery is separate from
lifecycle, and the registry itself contains no device-specific behavior.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

from drone_hal.device import DeviceDescriptor
from drone_hal.driver import IHardwareDriver
from drone_hal.exceptions import DeviceAlreadyRegisteredError, DeviceNotFoundError

DriverFactory = Callable[[], IHardwareDriver]


class IHardwareRegistry(ABC):
    """Contract for registering and retrieving hardware drivers."""

    @abstractmethod
    def register(self, descriptor: DeviceDescriptor, factory: DriverFactory) -> None:
        """
        Register a driver factory under ``descriptor.device_id``.

        Raises DeviceAlreadyRegisteredError if that device id is already
        registered.
        """

    @abstractmethod
    def unregister(self, device_id: str) -> None:
        """Remove a device from the registry, discarding any live instance."""

    @abstractmethod
    def get(self, device_id: str) -> IHardwareDriver:
        """
        Return the driver instance for ``device_id``.

        Instantiated lazily on first access. Raises DeviceNotFoundError
        if ``device_id`` is not registered.
        """

    @abstractmethod
    def list_devices(self) -> list[DeviceDescriptor]:
        """Return descriptors for every registered device."""

    @abstractmethod
    def instantiated_devices(self) -> list[str]:
        """Return device ids whose driver has already been instantiated."""


class HardwareRegistry(IHardwareRegistry):
    """In-memory hardware registry; one instance is owned by HardwareManager."""

    def __init__(self) -> None:
        self._descriptors: dict[str, DeviceDescriptor] = {}
        self._factories: dict[str, DriverFactory] = {}
        self._instances: dict[str, IHardwareDriver] = {}

    def register(self, descriptor: DeviceDescriptor, factory: DriverFactory) -> None:
        if descriptor.device_id in self._descriptors:
            raise DeviceAlreadyRegisteredError(
                f'{descriptor.device_id} is already registered',
            )
        self._descriptors[descriptor.device_id] = descriptor
        self._factories[descriptor.device_id] = factory

    def unregister(self, device_id: str) -> None:
        self._descriptors.pop(device_id, None)
        self._factories.pop(device_id, None)
        self._instances.pop(device_id, None)

    def get(self, device_id: str) -> IHardwareDriver:
        if device_id not in self._factories:
            raise DeviceNotFoundError(f'{device_id} is not registered')
        if device_id not in self._instances:
            self._instances[device_id] = self._factories[device_id]()
        return self._instances[device_id]

    def list_devices(self) -> list[DeviceDescriptor]:
        return list(self._descriptors.values())

    def instantiated_devices(self) -> list[str]:
        return list(self._instances.keys())
