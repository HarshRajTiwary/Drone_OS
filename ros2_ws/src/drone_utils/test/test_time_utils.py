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

"""Unit tests for time_utils."""

from drone_utils.time_utils import (
    monotonic_now,
    ros_time_from_seconds,
    seconds_from_ros_time,
    utc_now_iso,
)


def test_ros_time_round_trip():
    original = 1752345678.123456
    ros_time = ros_time_from_seconds(original)
    recovered = seconds_from_ros_time(ros_time)
    assert abs(recovered - original) < 1e-6


def test_ros_time_from_seconds_splits_sec_and_nanosec():
    ros_time = ros_time_from_seconds(10.5)
    assert ros_time.sec == 10
    assert ros_time.nanosec == 500000000


def test_monotonic_now_is_non_decreasing():
    first = monotonic_now()
    second = monotonic_now()
    assert second >= first


def test_utc_now_iso_ends_with_z():
    assert utc_now_iso().endswith('Z')
