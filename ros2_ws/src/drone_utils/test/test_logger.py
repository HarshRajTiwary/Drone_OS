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

"""Unit tests for CentralLogger."""

import logging

from drone_utils.logger import CentralLogger


class _FakeRosLogger:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def debug(self, msg):
        self.calls.append(('debug', msg))

    def info(self, msg):
        self.calls.append(('info', msg))

    def warn(self, msg):
        self.calls.append(('warn', msg))

    def error(self, msg):
        self.calls.append(('error', msg))

    def fatal(self, msg):
        self.calls.append(('fatal', msg))


def test_logs_reach_stdlib_logging():
    records: list[logging.LogRecord] = []

    class _CollectingHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    logger = CentralLogger('boot_manager', subsystem='core')
    named_logger = logging.getLogger('droneos.boot_manager.core')
    handler = _CollectingHandler(level=logging.INFO)
    named_logger.addHandler(handler)
    named_logger.setLevel(logging.INFO)
    try:
        logger.info('ready')
    finally:
        named_logger.removeHandler(handler)

    assert any('ready' in record.getMessage() for record in records)


def test_with_subsystem_returns_new_bound_logger():
    logger = CentralLogger('boot_manager', subsystem='core')
    bound = logger.with_subsystem('health_manager')
    assert bound is not logger


def test_warning_maps_to_ros_warn():
    ros_logger = _FakeRosLogger()
    logger = CentralLogger('boot_manager', ros_logger=ros_logger)
    logger.warning('low battery')
    assert ros_logger.calls[0][0] == 'warn'


def test_critical_maps_to_ros_fatal():
    ros_logger = _FakeRosLogger()
    logger = CentralLogger('boot_manager', ros_logger=ros_logger)
    logger.critical('unrecoverable fault')
    assert ros_logger.calls[0][0] == 'fatal'


def test_context_is_included_in_forwarded_message():
    ros_logger = _FakeRosLogger()
    logger = CentralLogger('boot_manager', ros_logger=ros_logger)
    logger.error('config invalid', key='safety.max_altitude_m')
    assert 'key' in ros_logger.calls[0][1]
