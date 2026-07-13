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
Configuration provider contract.

Per docs/phase0/configuration_strategy.md, configuration is organized into a
fixed set of YAML-driven domains. drone_utils implements IConfigurationProvider;
consumers depend only on this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class ConfigDomain(Enum):
    """Configuration hierarchy domains defined by the configuration strategy."""

    GLOBAL = 'global'
    MISSION = 'mission'
    HARDWARE = 'hardware'
    SAFETY = 'safety'
    LOGGING = 'logging'


class IConfigurationProvider(ABC):
    """Contract for loading, validating, and exposing YAML configuration."""

    @abstractmethod
    def get(self, domain: ConfigDomain, key: str, default: Any = None) -> Any:
        """Return a single value from ``domain`` using dotted ``key`` notation."""

    @abstractmethod
    def get_section(self, domain: ConfigDomain) -> dict[str, Any]:
        """Return the full configuration mapping for ``domain``."""

    @abstractmethod
    def reload(self) -> None:
        """
        Reload configuration from its backing source(s).

        Raises ConfigurationError if the reloaded configuration fails validation.
        """

    @abstractmethod
    def validate(self) -> list[str]:
        """
        Validate currently loaded configuration.

        Returns a list of human-readable validation error messages; empty
        if the current configuration is valid.
        """
