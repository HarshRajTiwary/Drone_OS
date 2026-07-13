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
Centralized logger contract.

Level names follow Python's standard logging module rather than ROS 2's
DEBUG/INFO/WARN/ERROR/FATAL naming; drone_utils's rclpy bridge is
responsible for mapping WARNING->WARN and CRITICAL->FATAL when it forwards
records to rosout.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from time import time


class LogLevel(IntEnum):
    """Supported log severities, ordered least to most severe."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclass(frozen=True)
class LogRecord:
    """A single structured log entry."""

    timestamp: float
    level: LogLevel
    node_name: str
    subsystem: str
    message: str
    correlation_id: str | None = None
    context: dict[str, object] = field(default_factory=dict)


class ILogger(ABC):
    """Contract for the centralized DroneOS logger."""

    @abstractmethod
    def debug(self, message: str, **context: object) -> None:
        """Log at DEBUG severity."""

    @abstractmethod
    def info(self, message: str, **context: object) -> None:
        """Log at INFO severity."""

    @abstractmethod
    def warning(self, message: str, **context: object) -> None:
        """Log at WARNING severity."""

    @abstractmethod
    def error(self, message: str, **context: object) -> None:
        """Log at ERROR severity."""

    @abstractmethod
    def critical(self, message: str, **context: object) -> None:
        """Log at CRITICAL severity."""

    @abstractmethod
    def with_subsystem(self, subsystem: str) -> 'ILogger':
        """Return a logger bound to ``subsystem`` for subsequent calls."""


def now() -> float:
    """Return the current epoch time, used by ILogger implementations."""
    return time()
