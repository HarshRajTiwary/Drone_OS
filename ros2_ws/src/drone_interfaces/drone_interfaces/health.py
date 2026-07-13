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

"""Health monitoring contract for CPU/RAM/disk/ROS/node/heartbeat checks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from time import time


class HealthStatus(Enum):
    """Aggregate or per-component health state, ordered least to most severe."""

    OK = 'ok'
    DEGRADED = 'degraded'
    WARNING = 'warning'
    CRITICAL = 'critical'
    UNKNOWN = 'unknown'


@dataclass(frozen=True)
class HealthReport:
    """Health snapshot produced by a single checkable component."""

    component: str
    status: HealthStatus
    message: str
    timestamp: float = field(default_factory=time)
    metrics: dict[str, float] = field(default_factory=dict)


class IHealthCheckable(ABC):
    """Contract for any component that can report its own health."""

    @abstractmethod
    def check_health(self) -> HealthReport:
        """Return a current health report for this component."""


class IHealthMonitor(ABC):
    """
    Contract for the platform Health Manager.

    Aggregates HealthReports from registered IHealthCheckable components
    (CPU, RAM, disk, ROS graph status, node status, heartbeat, and future
    hardware checks) into an overall platform health state.
    """

    @abstractmethod
    def register(self, component: IHealthCheckable) -> None:
        """Register a component to be included in health collection."""

    @abstractmethod
    def unregister(self, component_name: str) -> None:
        """Remove a previously registered component by name."""

    @abstractmethod
    def collect(self) -> list[HealthReport]:
        """Poll every registered component and return their current reports."""

    @abstractmethod
    def overall_status(self) -> HealthStatus:
        """Return the worst status across all registered components."""
