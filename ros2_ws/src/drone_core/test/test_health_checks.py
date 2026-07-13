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

"""Unit tests for the concrete IHealthCheckable implementations."""

from drone_core.health_checks import (
    CpuHealthCheck,
    DiskHealthCheck,
    HeartbeatHealthCheck,
    RamHealthCheck,
    RosGraphHealthCheck,
)
from drone_interfaces.health import HealthStatus


def test_cpu_check_returns_report_with_load_metrics():
    report = CpuHealthCheck().check_health()
    assert report.component == 'cpu'
    assert 'load_1min' in report.metrics
    assert report.status in set(HealthStatus)


def test_ram_check_returns_used_percent():
    report = RamHealthCheck().check_health()
    assert report.component == 'ram'
    assert 0.0 <= report.metrics['used_percent'] <= 100.0


def test_disk_check_returns_used_percent_for_root():
    report = DiskHealthCheck(path='/').check_health()
    assert report.component == 'disk'
    assert 0.0 <= report.metrics['used_percent'] <= 100.0


def test_cpu_check_reaches_critical_at_low_threshold():
    report = CpuHealthCheck(degraded_percent=0.0, warn_percent=0.0, critical_percent=0.0)
    assert report.check_health().status is HealthStatus.CRITICAL


def test_heartbeat_ok_immediately_after_construction():
    check = HeartbeatHealthCheck(stale_after_s=5.0)
    assert check.check_health().status is HealthStatus.OK


def test_heartbeat_critical_when_stale():
    check = HeartbeatHealthCheck(stale_after_s=-1.0)
    assert check.check_health().status is HealthStatus.CRITICAL


def test_heartbeat_beat_resets_staleness():
    check = HeartbeatHealthCheck(stale_after_s=5.0)
    check.beat()
    assert check.check_health().status is HealthStatus.OK


def test_ros_graph_check_reports_unknown_without_a_node():
    report = RosGraphHealthCheck(ros_node=None).check_health()
    assert report.status is HealthStatus.UNKNOWN
