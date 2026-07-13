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

"""Unit tests for the diagnostics publishing contract."""

from drone_interfaces.diagnostics import (
    DiagnosticItem,
    DiagnosticLevel,
    DiagnosticReport,
    IDiagnosticsPublisher,
)
import pytest


class _FakePublisher(IDiagnosticsPublisher):
    def __init__(self) -> None:
        self.published: list[DiagnosticReport] = []

    def publish(self, report):
        self.published.append(report)

    def publish_all(self, reports):
        self.published.extend(reports)


def test_diagnostic_level_matches_diagnostic_msgs_wire_values():
    assert DiagnosticLevel.OK == 0
    assert DiagnosticLevel.WARN == 1
    assert DiagnosticLevel.ERROR == 2
    assert DiagnosticLevel.STALE == 3


def test_cannot_instantiate_abstract_publisher():
    with pytest.raises(TypeError):
        IDiagnosticsPublisher()


def test_fake_publisher_records_single_report():
    publisher = _FakePublisher()
    report = DiagnosticReport(
        name='health_manager', level=DiagnosticLevel.OK, message='nominal',
        items=(DiagnosticItem(key='cpu_percent', value='12.5'),),
    )
    publisher.publish(report)
    assert publisher.published == [report]


def test_fake_publisher_records_batch():
    publisher = _FakePublisher()
    reports = [
        DiagnosticReport(name='cpu', level=DiagnosticLevel.OK, message='ok'),
        DiagnosticReport(name='disk', level=DiagnosticLevel.WARN, message='low space'),
    ]
    publisher.publish_all(reports)
    assert publisher.published == reports


def test_diagnostic_report_hardware_id_defaults_to_empty_string():
    report = DiagnosticReport(name='cpu', level=DiagnosticLevel.OK, message='ok')
    assert report.hardware_id == ''
    assert report.items == ()
