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

"""Unit tests for the DroneOS exception hierarchy."""

from drone_interfaces.exceptions import (
    ConfigurationError,
    DependencyResolutionError,
    DroneOSError,
    HealthCheckError,
    LifecycleError,
    MissionError,
    StateTransitionError,
    ValidationError,
)

ALL_SUBCLASSES = (
    ConfigurationError,
    ValidationError,
    LifecycleError,
    StateTransitionError,
    HealthCheckError,
    MissionError,
    DependencyResolutionError,
)


def test_all_exceptions_derive_from_drone_os_error():
    for exc_type in ALL_SUBCLASSES:
        assert issubclass(exc_type, DroneOSError)


def test_drone_os_error_derives_from_exception():
    assert issubclass(DroneOSError, Exception)


def test_exception_carries_message():
    err = ConfigurationError('missing safety.max_altitude_m')
    assert str(err) == 'missing safety.max_altitude_m'
