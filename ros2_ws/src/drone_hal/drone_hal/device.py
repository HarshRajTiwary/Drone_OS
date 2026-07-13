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
Generic device identity and presence model shared by every HAL driver.

Lifecycle stage and health are intentionally not redefined here: drivers
reuse drone_interfaces.lifecycle.LifecycleState and
drone_interfaces.health.HealthStatus directly (see driver.py). This module
only adds the one axis those contracts do not cover: whether the physical
device is currently present on its bus.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class BusType(Enum):
    """Physical or logical bus a device is attached to."""

    UART = 'uart'
    SPI = 'spi'
    I2C = 'i2c'
    CSI = 'csi'
    USB = 'usb'
    GPIO = 'gpio'


class DeviceConnectivity(Enum):
    """Physical presence of a device, independent of its lifecycle stage."""

    UNKNOWN = 'unknown'
    PRESENT = 'present'
    MISSING = 'missing'
    DISCONNECTED = 'disconnected'


@dataclass(frozen=True)
class DeviceDescriptor:
    """
    Static identity of a hardware device, as declared in YAML configuration.

    ``driver_class`` is a dotted ``module:ClassName`` path resolved by
    IDriverLoader; ``address`` is bus-specific (e.g. a device file path for
    UART/SPI/I2C, or a USB vendor:product id).
    """

    device_id: str
    device_type: str
    bus: BusType
    address: str
    driver_class: str
    metadata: dict[str, str] = field(default_factory=dict)
