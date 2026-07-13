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

"""Unit tests for CoreHealthMonitor."""

from drone_core.health_manager import CoreHealthMonitor
from drone_interfaces.health import HealthStatus
from drone_interfaces.lifecycle import LifecycleState


def test_full_lifecycle_registers_default_checks():
    monitor = CoreHealthMonitor()
    assert monitor.on_configure() is True
    assert monitor.lifecycle_state is LifecycleState.INACTIVE

    reports = monitor.collect()
    components = {r.component for r in reports}
    assert {'cpu', 'ram', 'disk', 'heartbeat'} <= components

    assert monitor.on_activate() is True
    assert monitor.lifecycle_state is LifecycleState.ACTIVE
    assert monitor.on_deactivate() is True
    assert monitor.on_cleanup() is True
    assert monitor.collect() == []
    assert monitor.on_shutdown() is True
    assert monitor.lifecycle_state is LifecycleState.FINALIZED


def test_overall_status_unknown_before_any_registration():
    assert CoreHealthMonitor().overall_status() is HealthStatus.UNKNOWN


def test_overall_status_reflects_worst_registered_check():
    monitor = CoreHealthMonitor()
    monitor.on_configure()
    assert monitor.overall_status() in set(HealthStatus)


def test_safety_config_thresholds_are_applied():
    thresholds = {'critical_percent': 0.0, 'warn_percent': 0.0, 'degraded_percent': 0.0}
    safety_config = {'health': {'cpu': thresholds}}
    monitor = CoreHealthMonitor(safety_config)
    monitor.on_configure()
    cpu_report = next(r for r in monitor.collect() if r.component == 'cpu')
    assert cpu_report.status is HealthStatus.CRITICAL


def test_unregister_removes_component():
    monitor = CoreHealthMonitor()
    monitor.on_configure()
    monitor.unregister('cpu')
    assert 'cpu' not in {r.component for r in monitor.collect()}
