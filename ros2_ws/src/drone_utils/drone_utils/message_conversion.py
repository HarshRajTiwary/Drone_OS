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
Conversion between drone_interfaces Python contracts and drone_msgs wire types.

Neither of those two packages may depend on the other (see
drone_msgs/docs/interfaces.md), so this is the one place the mapping
lives. Mappings are keyed by enum member, not numeric value, so they stay
correct even though the Python enums (Enum.auto(), 1-indexed) and the
ROS msg constants (0-indexed by convention) do not numerically align.
"""

from __future__ import annotations

from diagnostic_msgs.msg import KeyValue
from drone_interfaces.health import HealthReport, HealthStatus
from drone_interfaces.mission import MissionMetadata, MissionState
from drone_interfaces.state_machine import SystemState
from drone_msgs.msg import HealthReport as HealthReportMsg
from drone_msgs.msg import MissionInfo as MissionInfoMsg
from drone_msgs.msg import SystemState as SystemStateMsg

from drone_utils.time_utils import ros_time_from_seconds, seconds_from_ros_time

_STATE_TO_MSG = {
    SystemState.BOOTING: SystemStateMsg.BOOTING,
    SystemState.INITIALIZING: SystemStateMsg.INITIALIZING,
    SystemState.READY: SystemStateMsg.READY,
    SystemState.MISSION_RUNNING: SystemStateMsg.MISSION_RUNNING,
    SystemState.PAUSED: SystemStateMsg.PAUSED,
    SystemState.ERROR: SystemStateMsg.ERROR,
    SystemState.SHUTDOWN: SystemStateMsg.SHUTDOWN,
}
_MSG_TO_STATE = {value: key for key, value in _STATE_TO_MSG.items()}

_HEALTH_TO_MSG = {
    HealthStatus.OK: HealthReportMsg.OK,
    HealthStatus.DEGRADED: HealthReportMsg.DEGRADED,
    HealthStatus.WARNING: HealthReportMsg.WARNING,
    HealthStatus.CRITICAL: HealthReportMsg.CRITICAL,
    HealthStatus.UNKNOWN: HealthReportMsg.UNKNOWN,
}
_MSG_TO_HEALTH = {value: key for key, value in _HEALTH_TO_MSG.items()}

_MISSION_STATE_TO_MSG = {
    MissionState.UNINITIALIZED: MissionInfoMsg.UNINITIALIZED,
    MissionState.INITIALIZED: MissionInfoMsg.INITIALIZED,
    MissionState.RUNNING: MissionInfoMsg.RUNNING,
    MissionState.PAUSED: MissionInfoMsg.PAUSED,
    MissionState.COMPLETED: MissionInfoMsg.COMPLETED,
    MissionState.ABORTED: MissionInfoMsg.ABORTED,
    MissionState.FAILED: MissionInfoMsg.FAILED,
}
_MSG_TO_MISSION_STATE = {value: key for key, value in _MISSION_STATE_TO_MSG.items()}


def system_state_to_msg(state: SystemState, reason: str, timestamp: float) -> SystemStateMsg:
    """Convert a SystemState + reason + epoch timestamp to a SystemState message."""
    return SystemStateMsg(
        state=_STATE_TO_MSG[state], reason=reason,
        stamp=ros_time_from_seconds(timestamp),
    )


def system_state_from_msg(msg: SystemStateMsg) -> tuple[SystemState, str, float]:
    """Convert a SystemState message back to (SystemState, reason, epoch timestamp)."""
    return _MSG_TO_STATE[msg.state], msg.reason, seconds_from_ros_time(msg.stamp)


def health_report_to_msg(report: HealthReport) -> HealthReportMsg:
    """Convert a drone_interfaces HealthReport to a drone_msgs HealthReport message."""
    return HealthReportMsg(
        component=report.component,
        status=_HEALTH_TO_MSG[report.status],
        message=report.message,
        stamp=ros_time_from_seconds(report.timestamp),
        metrics=[KeyValue(key=k, value=str(v)) for k, v in report.metrics.items()],
    )


def health_report_from_msg(msg: HealthReportMsg) -> HealthReport:
    """Convert a drone_msgs HealthReport message to a drone_interfaces HealthReport."""
    return HealthReport(
        component=msg.component,
        status=_MSG_TO_HEALTH[msg.status],
        message=msg.message,
        timestamp=seconds_from_ros_time(msg.stamp),
        metrics={item.key: item.value for item in msg.metrics},
    )


def mission_info_to_msg(metadata: MissionMetadata, state: MissionState) -> MissionInfoMsg:
    """Convert MissionMetadata + MissionState to a MissionInfo message."""
    return MissionInfoMsg(
        name=metadata.name, version=metadata.version, description=metadata.description,
        state=_MISSION_STATE_TO_MSG[state],
    )


def mission_state_from_msg(msg: MissionInfoMsg) -> MissionState:
    """Extract the MissionState from a MissionInfo message."""
    return _MSG_TO_MISSION_STATE[msg.state]
