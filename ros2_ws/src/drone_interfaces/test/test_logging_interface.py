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

"""Unit tests for the ILogger contract and LogLevel ordering."""

from drone_interfaces.logging import ILogger, LogLevel, LogRecord
import pytest


class _FakeLogger(ILogger):
    def __init__(self, subsystem: str = 'root') -> None:
        self.subsystem = subsystem
        self.records: list[tuple[LogLevel, str]] = []

    def debug(self, message, **context):
        self.records.append((LogLevel.DEBUG, message))

    def info(self, message, **context):
        self.records.append((LogLevel.INFO, message))

    def warning(self, message, **context):
        self.records.append((LogLevel.WARNING, message))

    def error(self, message, **context):
        self.records.append((LogLevel.ERROR, message))

    def critical(self, message, **context):
        self.records.append((LogLevel.CRITICAL, message))

    def with_subsystem(self, subsystem):
        return _FakeLogger(subsystem)


def test_log_level_matches_required_severities():
    assert {level.name for level in LogLevel} == {
        'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
    }


def test_log_level_ordering_is_monotonic():
    assert LogLevel.DEBUG < LogLevel.INFO < LogLevel.WARNING < LogLevel.ERROR < LogLevel.CRITICAL


def test_cannot_instantiate_abstract_logger():
    with pytest.raises(TypeError):
        ILogger()


def test_fake_logger_records_messages_at_correct_level():
    logger = _FakeLogger()
    logger.info('boot manager starting')
    logger.error('config validation failed')
    assert logger.records == [
        (LogLevel.INFO, 'boot manager starting'),
        (LogLevel.ERROR, 'config validation failed'),
    ]


def test_with_subsystem_returns_bound_logger():
    logger = _FakeLogger().with_subsystem('health_manager')
    assert logger.subsystem == 'health_manager'


def test_log_record_is_frozen_and_defaults_context_to_empty_dict():
    record = LogRecord(
        timestamp=0.0, level=LogLevel.INFO, node_name='boot_manager',
        subsystem='core', message='ready',
    )
    assert record.context == {}
    with pytest.raises(AttributeError):
        record.message = 'mutated'
