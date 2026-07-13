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

"""Integration tests for BootManager end-to-end boot/shutdown sequence."""

from drone_core.boot_manager import BootManager
from drone_interfaces.health import HealthStatus
from drone_interfaces.lifecycle import LifecycleState
from drone_interfaces.state_machine import SystemState


def test_boot_reaches_ready(tmp_path):
    manager = BootManager(str(tmp_path))
    assert manager.boot() is True
    assert manager.state_machine.current_state is SystemState.READY


def test_boot_activates_health_and_mission_managers(tmp_path):
    manager = BootManager(str(tmp_path))
    manager.boot()
    assert manager.health_monitor.lifecycle_state is LifecycleState.ACTIVE
    assert manager.mission_registry.lifecycle_state is LifecycleState.ACTIVE


def test_boot_populates_diagnostics(tmp_path):
    manager = BootManager(str(tmp_path))
    manager.boot()
    reports = manager.health_monitor.collect()
    assert {'cpu', 'ram', 'disk', 'heartbeat'} <= {r.component for r in reports}


def test_shutdown_reaches_shutdown_state(tmp_path):
    manager = BootManager(str(tmp_path))
    manager.boot()
    assert manager.shutdown() is True
    assert manager.state_machine.current_state is SystemState.SHUTDOWN


def test_boot_applies_safety_config_thresholds(tmp_path):
    (tmp_path / 'safety_config.yaml').write_text(
        'health:\n  cpu:\n    critical_percent: 0.0\n    warn_percent: 0.0\n'
        '    degraded_percent: 0.0\n',
    )
    manager = BootManager(str(tmp_path))
    manager.boot()
    cpu_report = next(r for r in manager.health_monitor.collect() if r.component == 'cpu')
    assert cpu_report.status is HealthStatus.CRITICAL
