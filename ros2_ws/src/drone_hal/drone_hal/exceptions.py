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
HAL-specific exceptions.

All derive from drone_interfaces.exceptions.DroneOSError so callers can
catch either the specific HAL condition or the platform-wide base class.
"""

from __future__ import annotations

from drone_interfaces.exceptions import DroneOSError


class DeviceNotFoundError(DroneOSError):
    """Raised when a requested device id is not present in the registry."""


class DeviceAlreadyRegisteredError(DroneOSError):
    """Raised when registering a device id that is already registered."""


class DriverLoadError(DroneOSError):
    """Raised when a configured driver class cannot be imported or is invalid."""


class DeviceDiscoveryError(DroneOSError):
    """Raised when bus discovery cannot be completed for a device descriptor."""
