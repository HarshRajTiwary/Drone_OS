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
Dynamic driver loader.

Resolves the ``driver_class`` dotted path on a DeviceDescriptor (e.g.
``"drone_camera.driver:PiCameraDriver"``) into an importable class,
without drone_hal ever importing a device-specific package directly. This
is what lets new hardware packages plug into the HAL purely through YAML
configuration: drone_hal never needs a code change to support a new
camera or flight controller implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import importlib

from drone_hal.driver import IHardwareDriver
from drone_hal.exceptions import DriverLoadError


class IDriverLoader(ABC):
    """Contract for resolving a driver class reference into a usable type."""

    @abstractmethod
    def load(self, driver_class: str) -> type[IHardwareDriver]:
        """
        Resolve ``driver_class`` (``"module.path:ClassName"``) to a type.

        Raises DriverLoadError if the module cannot be imported, the
        class does not exist, or it is not a subclass of IHardwareDriver.
        """


class DriverLoader(IDriverLoader):
    """Imports driver classes by dotted ``module:ClassName`` reference."""

    def load(self, driver_class: str) -> type[IHardwareDriver]:
        if ':' not in driver_class:
            raise DriverLoadError(
                f'{driver_class!r} is not in "module.path:ClassName" form',
            )
        module_path, _, class_name = driver_class.partition(':')
        try:
            module = importlib.import_module(module_path)
        except ImportError as exc:
            raise DriverLoadError(f'cannot import {module_path!r}: {exc}') from exc

        driver_cls = getattr(module, class_name, None)
        if driver_cls is None:
            raise DriverLoadError(f'{class_name!r} not found in {module_path!r}')
        if not (isinstance(driver_cls, type) and issubclass(driver_cls, IHardwareDriver)):
            raise DriverLoadError(
                f'{driver_class!r} does not subclass IHardwareDriver',
            )
        return driver_cls
