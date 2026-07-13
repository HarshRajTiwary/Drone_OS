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

"""Unit tests for error_helpers."""

from drone_interfaces.exceptions import ConfigurationError, DroneOSError
from drone_utils.error_helpers import error_boundary, retry
import pytest


class _RecordingLogger:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, message, **context):
        self.errors.append(message)


def test_error_boundary_passes_through_drone_os_error():
    logger = _RecordingLogger()
    with pytest.raises(ConfigurationError):
        with error_boundary(logger, 'config'):
            raise ConfigurationError('bad config')
    assert logger.errors


def test_error_boundary_wraps_generic_exception():
    logger = _RecordingLogger()
    with pytest.raises(DroneOSError):
        with error_boundary(logger, 'config'):
            raise ValueError('boom')
    assert logger.errors


def test_error_boundary_does_not_swallow_success():
    logger = _RecordingLogger()
    with error_boundary(logger, 'config'):
        pass
    assert logger.errors == []


def test_retry_returns_on_first_success():
    calls = []

    @retry(times=3)
    def flaky():
        calls.append(1)
        return 'ok'

    assert flaky() == 'ok'
    assert len(calls) == 1


def test_retry_retries_up_to_limit_then_raises():
    calls = []

    @retry(times=3, exceptions=(ValueError,))
    def always_fails():
        calls.append(1)
        raise ValueError('nope')

    with pytest.raises(ValueError):
        always_fails()
    assert len(calls) == 3


def test_retry_rejects_non_positive_times():
    with pytest.raises(ValueError):
        retry(times=0)
