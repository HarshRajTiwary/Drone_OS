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

"""Exception hierarchy shared by all DroneOS platform packages."""

from __future__ import annotations


class DroneOSError(Exception):
    """Base class for all DroneOS platform exceptions."""


class ConfigurationError(DroneOSError):
    """Raised when configuration is missing, malformed, or fails validation."""


class ValidationError(DroneOSError):
    """Raised when a value fails schema, range, or type validation."""


class LifecycleError(DroneOSError):
    """Raised when a lifecycle transition is invalid or a lifecycle hook fails."""


class StateTransitionError(DroneOSError):
    """Raised when a state machine transition is not permitted."""


class HealthCheckError(DroneOSError):
    """Raised when a health check cannot be completed or reports a fatal fault."""


class MissionError(DroneOSError):
    """Raised for mission registration, activation, or execution failures."""


class DependencyResolutionError(DroneOSError):
    """Raised when a dependency-injection container cannot resolve a dependency."""
