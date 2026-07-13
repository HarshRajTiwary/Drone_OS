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
Diagnostics publishing contract.

DiagnosticLevel values match diagnostic_msgs/DiagnosticStatus (OK=0, WARN=1,
ERROR=2, STALE=3) so drone_dashboard can bridge reports onto the standard
/diagnostics topic without a translation table.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum


class DiagnosticLevel(IntEnum):
    """Severity levels wire-compatible with diagnostic_msgs/DiagnosticStatus."""

    OK = 0
    WARN = 1
    ERROR = 2
    STALE = 3


@dataclass(frozen=True)
class DiagnosticItem:
    """A single key/value diagnostic datum."""

    key: str
    value: str


@dataclass(frozen=True)
class DiagnosticReport:
    """A named diagnostic status for one subsystem or hardware id."""

    name: str
    level: DiagnosticLevel
    message: str
    hardware_id: str = ''
    items: tuple[DiagnosticItem, ...] = field(default_factory=tuple)


class IDiagnosticsPublisher(ABC):
    """Contract for publishing diagnostic reports from platform services."""

    @abstractmethod
    def publish(self, report: DiagnosticReport) -> None:
        """Publish a single diagnostic report."""

    @abstractmethod
    def publish_all(self, reports: list[DiagnosticReport]) -> None:
        """Publish a batch of diagnostic reports as one array update."""
