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

"""Package version lookup and simple semantic-version comparison."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory, PackageNotFoundError
from drone_interfaces.exceptions import ValidationError


def get_package_version(package_name: str) -> str:
    """Return the version string from an installed ROS 2 package's package.xml."""
    try:
        share_dir = get_package_share_directory(package_name)
    except PackageNotFoundError:
        return 'unknown'
    try:
        tree = ET.parse(f'{share_dir}/package.xml')
        version_element = tree.getroot().find('version')
        return version_element.text.strip() if version_element is not None else 'unknown'
    except (OSError, ET.ParseError):
        return 'unknown'


def parse_semver(version: str) -> tuple[int, int, int]:
    """Parse a "major.minor.patch" string into a 3-tuple of ints."""
    parts = version.split('.')
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValidationError(f'{version!r} is not a valid major.minor.patch version')
    major, minor, patch = (int(p) for p in parts)
    return major, minor, patch


def compare_versions(left: str, right: str) -> int:
    """Return -1, 0, or 1 comparing two "major.minor.patch" version strings."""
    left_tuple, right_tuple = parse_semver(left), parse_semver(right)
    if left_tuple < right_tuple:
        return -1
    if left_tuple > right_tuple:
        return 1
    return 0
