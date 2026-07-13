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

"""Unit tests for message_conversion (drone_interfaces <-> drone_msgs)."""

from drone_interfaces.health import HealthReport, HealthStatus
from drone_interfaces.mission import MissionMetadata, MissionState
from drone_interfaces.state_machine import SystemState
from drone_utils.message_conversion import (
    health_report_from_msg,
    health_report_to_msg,
    mission_info_to_msg,
    mission_state_from_msg,
    system_state_from_msg,
    system_state_to_msg,
)


def test_system_state_round_trip():
    msg = system_state_to_msg(SystemState.READY, 'boot complete', 1000.0)
    state, reason, timestamp = system_state_from_msg(msg)
    assert state is SystemState.READY
    assert reason == 'boot complete'
    assert abs(timestamp - 1000.0) < 1e-6


def test_every_system_state_converts():
    for state in SystemState:
        msg = system_state_to_msg(state, '', 0.0)
        recovered, _, _ = system_state_from_msg(msg)
        assert recovered is state


def test_health_report_round_trip():
    report = HealthReport(
        component='cpu', status=HealthStatus.DEGRADED, message='high load',
        timestamp=500.0, metrics={'load_percent': 87.5},
    )
    msg = health_report_to_msg(report)
    recovered = health_report_from_msg(msg)
    assert recovered.component == 'cpu'
    assert recovered.status is HealthStatus.DEGRADED
    assert recovered.metrics == {'load_percent': '87.5'}


def test_every_health_status_converts():
    for status in HealthStatus:
        report = HealthReport(component='x', status=status, message='', timestamp=0.0)
        msg = health_report_to_msg(report)
        assert health_report_from_msg(msg).status is status


def test_mission_info_round_trip():
    metadata = MissionMetadata(name='qr_landing', version='0.1.0', description='d')
    msg = mission_info_to_msg(metadata, MissionState.RUNNING)
    assert msg.name == 'qr_landing'
    assert mission_state_from_msg(msg) is MissionState.RUNNING


def test_every_mission_state_converts():
    metadata = MissionMetadata(name='x', version='0.1.0', description='')
    for state in MissionState:
        msg = mission_info_to_msg(metadata, state)
        assert mission_state_from_msg(msg) is state
