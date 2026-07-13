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

"""Unit tests for YamlConfigurationProvider."""

from drone_interfaces.configuration import ConfigDomain
from drone_utils.config_loader import YamlConfigurationProvider


def test_missing_config_dir_yields_empty_sections(tmp_path):
    provider = YamlConfigurationProvider(str(tmp_path))
    for domain in ConfigDomain:
        assert provider.get_section(domain) == {}


def test_loads_declared_domain_file(tmp_path):
    (tmp_path / 'safety_config.yaml').write_text('max_altitude_m: 30\n')
    provider = YamlConfigurationProvider(str(tmp_path))
    assert provider.get(ConfigDomain.SAFETY, 'max_altitude_m') == 30


def test_get_returns_default_for_missing_key(tmp_path):
    provider = YamlConfigurationProvider(str(tmp_path))
    assert provider.get(ConfigDomain.GLOBAL, 'missing', default='x') == 'x'


def test_reload_picks_up_file_changes(tmp_path):
    config_file = tmp_path / 'global_config.yaml'
    config_file.write_text('log_level: INFO\n')
    provider = YamlConfigurationProvider(str(tmp_path))
    assert provider.get(ConfigDomain.GLOBAL, 'log_level') == 'INFO'

    config_file.write_text('log_level: DEBUG\n')
    provider.reload()
    assert provider.get(ConfigDomain.GLOBAL, 'log_level') == 'DEBUG'


def test_validate_returns_no_errors_for_well_formed_config(tmp_path):
    provider = YamlConfigurationProvider(str(tmp_path))
    assert provider.validate() == []
