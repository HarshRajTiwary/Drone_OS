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

"""Unit tests for version_utils."""

from drone_interfaces.exceptions import ValidationError
from drone_utils.version_utils import compare_versions, get_package_version, parse_semver
import pytest


def test_get_package_version_returns_unknown_for_missing_package():
    assert get_package_version('no_such_package_xyz') == 'unknown'


def test_get_package_version_reads_installed_package():
    assert get_package_version('drone_interfaces') == '0.1.0'


def test_parse_semver_valid():
    assert parse_semver('1.2.3') == (1, 2, 3)


def test_parse_semver_rejects_malformed_string():
    with pytest.raises(ValidationError):
        parse_semver('1.2')


def test_compare_versions_orders_correctly():
    assert compare_versions('0.1.0', '0.2.0') == -1
    assert compare_versions('1.0.0', '1.0.0') == 0
    assert compare_versions('2.0.0', '1.9.9') == 1
