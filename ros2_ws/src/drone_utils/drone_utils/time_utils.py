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

"""Time utilities: wall-clock/monotonic helpers and ROS time conversion."""

from __future__ import annotations

from datetime import datetime, timezone
import time

from builtin_interfaces.msg import Time as RosTime


def wall_clock_now() -> float:
    """Return the current epoch time in seconds (time.time())."""
    return time.time()


def monotonic_now() -> float:
    """Return a monotonic clock reading in seconds, safe for measuring durations."""
    return time.monotonic()


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string with a 'Z' suffix."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def ros_time_from_seconds(seconds: float) -> RosTime:
    """Convert an epoch float to a builtin_interfaces/Time message."""
    sec = int(seconds)
    nanosec = int(round((seconds - sec) * 1e9))
    return RosTime(sec=sec, nanosec=nanosec)


def seconds_from_ros_time(ros_time: RosTime) -> float:
    """Convert a builtin_interfaces/Time message to an epoch float."""
    return ros_time.sec + ros_time.nanosec / 1e9
