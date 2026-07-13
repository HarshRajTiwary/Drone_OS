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
Safe YAML load/dump helpers.

Isolated from IConfigurationProvider so they can be reused (e.g. by a
mission plugin loading its own YAML) without pulling in the
config-domain machinery.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from drone_interfaces.exceptions import ConfigurationError
import yaml


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    """
    Load and parse a YAML file, returning an empty dict if it is absent.

    Raises ConfigurationError if the file exists but fails to parse, or
    parses to something other than a mapping at the top level.
    """
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        with file_path.open(encoding='utf-8') as handle:
            parsed = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise ConfigurationError(f'{file_path}: invalid YAML: {exc}') from exc

    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise ConfigurationError(
            f'{file_path}: expected a mapping at the top level, got {type(parsed).__name__}',
        )
    return parsed


def dump_yaml_file(path: str | Path, data: dict[str, Any]) -> None:
    """Write ``data`` to ``path`` as YAML, creating parent directories as needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('w', encoding='utf-8') as handle:
        yaml.safe_dump(data, handle, sort_keys=False)


def get_dotted(data: dict[str, Any], dotted_key: str, default: Any = None) -> Any:
    """Return ``data['a']['b']`` for dotted_key ``"a.b"``, or ``default`` if absent."""
    current: Any = data
    for part in dotted_key.split('.'):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
