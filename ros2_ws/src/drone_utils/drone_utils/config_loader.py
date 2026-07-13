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
YAML configuration loader implementing drone_interfaces.configuration.IConfigurationProvider.

Per docs/phase0/configuration_strategy.md, configuration is split into
five domain files in one directory: global_config.yaml,
mission_config.yaml, hardware_config.yaml, safety_config.yaml,
logging_config.yaml. A missing file is not an error (that domain is
simply empty); a malformed one is.
"""

from __future__ import annotations

from typing import Any

from drone_interfaces.configuration import ConfigDomain, IConfigurationProvider

from drone_utils.yaml_parser import get_dotted, load_yaml_file

_DOMAIN_FILENAMES: dict[ConfigDomain, str] = {
    ConfigDomain.GLOBAL: 'global_config.yaml',
    ConfigDomain.MISSION: 'mission_config.yaml',
    ConfigDomain.HARDWARE: 'hardware_config.yaml',
    ConfigDomain.SAFETY: 'safety_config.yaml',
    ConfigDomain.LOGGING: 'logging_config.yaml',
}


class YamlConfigurationProvider(IConfigurationProvider):
    """Loads and serves the five DroneOS configuration domains from a directory."""

    def __init__(self, config_dir: str) -> None:
        self._config_dir = config_dir
        self._sections: dict[ConfigDomain, dict[str, Any]] = {}
        self.reload()

    def get(self, domain: ConfigDomain, key: str, default: Any = None) -> Any:
        return get_dotted(self._sections.get(domain, {}), key, default)

    def get_section(self, domain: ConfigDomain) -> dict[str, Any]:
        return dict(self._sections.get(domain, {}))

    def reload(self) -> None:
        loaded: dict[ConfigDomain, dict[str, Any]] = {}
        for domain, filename in _DOMAIN_FILENAMES.items():
            path = f'{self._config_dir}/{filename}'
            loaded[domain] = load_yaml_file(path)
        self._sections = loaded

    def validate(self) -> list[str]:
        errors: list[str] = []
        for domain in ConfigDomain:
            section = self._sections.get(domain, {})
            if not isinstance(section, dict):
                errors.append(f'{domain.value}: expected a mapping, got {type(section).__name__}')
        return errors
