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
Lifecycle contract implemented by every managed DroneOS component.

Mirrors the semantics of the ROS 2 managed-node lifecycle (configure,
activate, deactivate, cleanup, shutdown) so that both rclpy LifecycleNode
wrappers and plain platform services (e.g. the boot manager) can share one
contract and be driven identically by drone_core's Lifecycle Manager.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import auto, Enum


class LifecycleState(Enum):
    """Current lifecycle stage of a managed component."""

    UNCONFIGURED = auto()
    INACTIVE = auto()
    ACTIVE = auto()
    FINALIZED = auto()


class LifecycleComponent(ABC):
    """Contract for any component whose lifecycle is externally managed."""

    @property
    @abstractmethod
    def lifecycle_state(self) -> LifecycleState:
        """Return the component's current lifecycle state."""

    @abstractmethod
    def on_configure(self) -> bool:
        """Load resources and validate configuration. Return True on success."""

    @abstractmethod
    def on_activate(self) -> bool:
        """Begin active operation. Return True on success."""

    @abstractmethod
    def on_deactivate(self) -> bool:
        """Pause active operation while retaining configuration. Return True on success."""

    @abstractmethod
    def on_cleanup(self) -> bool:
        """Release configured resources, returning to UNCONFIGURED. Return True on success."""

    @abstractmethod
    def on_shutdown(self) -> bool:
        """Perform final teardown from any state. Return True on success."""

    @abstractmethod
    def on_error(self, error: Exception) -> bool:
        """Handle a fault raised during any transition. Return True if recovered."""
