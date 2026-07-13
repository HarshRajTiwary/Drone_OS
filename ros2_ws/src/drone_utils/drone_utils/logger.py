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
Central logger implementing drone_interfaces.logging.ILogger.

Every entry carries timestamp, node name, subsystem, level, and message
(per docs/phase0/logging_strategy.md's required log format). Emits to
Python's stdlib logging always, and additionally bridges to an rclpy
node's logger when one is supplied, mapping WARNING->WARN and
CRITICAL->FATAL since rclpy has no WARNING/CRITICAL severities.
"""

from __future__ import annotations

import logging as _stdlib_logging

from drone_interfaces.logging import ILogger, LogLevel, LogRecord, now

_LEVEL_TO_STDLIB = {
    LogLevel.DEBUG: _stdlib_logging.DEBUG,
    LogLevel.INFO: _stdlib_logging.INFO,
    LogLevel.WARNING: _stdlib_logging.WARNING,
    LogLevel.ERROR: _stdlib_logging.ERROR,
    LogLevel.CRITICAL: _stdlib_logging.CRITICAL,
}


class CentralLogger(ILogger):
    """DroneOS structured logger, optionally bridged to an rclpy node logger."""

    def __init__(
        self,
        node_name: str,
        subsystem: str = 'root',
        ros_logger=None,
    ) -> None:
        self._node_name = node_name
        self._subsystem = subsystem
        self._ros_logger = ros_logger
        self._py_logger = _stdlib_logging.getLogger(f'droneos.{node_name}.{subsystem}')

    def debug(self, message: str, **context: object) -> None:
        self._emit(LogLevel.DEBUG, message, context)

    def info(self, message: str, **context: object) -> None:
        self._emit(LogLevel.INFO, message, context)

    def warning(self, message: str, **context: object) -> None:
        self._emit(LogLevel.WARNING, message, context)

    def error(self, message: str, **context: object) -> None:
        self._emit(LogLevel.ERROR, message, context)

    def critical(self, message: str, **context: object) -> None:
        self._emit(LogLevel.CRITICAL, message, context)

    def with_subsystem(self, subsystem: str) -> ILogger:
        return CentralLogger(self._node_name, subsystem, self._ros_logger)

    def _emit(self, level: LogLevel, message: str, context: dict[str, object]) -> None:
        record = LogRecord(
            timestamp=now(), level=level, node_name=self._node_name,
            subsystem=self._subsystem, message=message, context=context,
        )
        formatted = f'[{record.subsystem}] {record.message}'
        if context:
            formatted += f' {context}'
        self._py_logger.log(_LEVEL_TO_STDLIB[level], formatted)
        if self._ros_logger is not None:
            self._forward_to_ros(level, formatted)

    def _forward_to_ros(self, level: LogLevel, formatted: str) -> None:
        if level is LogLevel.DEBUG:
            self._ros_logger.debug(formatted)
        elif level is LogLevel.INFO:
            self._ros_logger.info(formatted)
        elif level is LogLevel.WARNING:
            self._ros_logger.warn(formatted)
        elif level is LogLevel.ERROR:
            self._ros_logger.error(formatted)
        elif level is LogLevel.CRITICAL:
            self._ros_logger.fatal(formatted)
