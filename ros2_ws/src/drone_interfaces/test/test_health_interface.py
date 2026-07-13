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

"""Unit tests for the health monitoring contract."""

from drone_interfaces.health import (
    HealthReport,
    HealthStatus,
    IHealthCheckable,
    IHealthMonitor,
)
import pytest


class _FakeCheckable(IHealthCheckable):
    def __init__(self, name: str, status: HealthStatus) -> None:
        self._name = name
        self._status = status

    def check_health(self) -> HealthReport:
        return HealthReport(
            component=self._name, status=self._status, message='fake', timestamp=0.0,
        )


class _FakeHealthMonitor(IHealthMonitor):
    def __init__(self) -> None:
        self._components: dict[str, IHealthCheckable] = {}

    def register(self, component):
        report = component.check_health()
        self._components[report.component] = component

    def unregister(self, component_name):
        self._components.pop(component_name, None)

    def collect(self):
        return [c.check_health() for c in self._components.values()]

    def overall_status(self):
        order = list(HealthStatus)
        reports = self.collect()
        if not reports:
            return HealthStatus.UNKNOWN
        return max(reports, key=lambda r: order.index(r.status)).status


def test_cannot_instantiate_abstract_checkable():
    with pytest.raises(TypeError):
        IHealthCheckable()


def test_cannot_instantiate_abstract_monitor():
    with pytest.raises(TypeError):
        IHealthMonitor()


def test_monitor_collects_registered_component_reports():
    monitor = _FakeHealthMonitor()
    monitor.register(_FakeCheckable('cpu', HealthStatus.OK))
    monitor.register(_FakeCheckable('disk', HealthStatus.DEGRADED))
    reports = monitor.collect()
    assert {r.component for r in reports} == {'cpu', 'disk'}


def test_overall_status_returns_unknown_when_no_components_registered():
    monitor = _FakeHealthMonitor()
    assert monitor.overall_status() == HealthStatus.UNKNOWN


def test_health_report_metrics_default_to_empty_dict():
    report = HealthReport(
        component='cpu', status=HealthStatus.OK, message='nominal', timestamp=0.0,
    )
    assert report.metrics == {}
