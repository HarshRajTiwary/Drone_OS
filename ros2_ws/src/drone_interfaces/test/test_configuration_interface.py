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

"""Unit tests for the IConfigurationProvider contract."""

from drone_interfaces.configuration import ConfigDomain, IConfigurationProvider
import pytest


class _FakeConfigProvider(IConfigurationProvider):
    def __init__(self, sections: dict[ConfigDomain, dict]) -> None:
        self._sections = sections

    def get(self, domain, key, default=None):
        return self._sections.get(domain, {}).get(key, default)

    def get_section(self, domain):
        return dict(self._sections.get(domain, {}))

    def reload(self) -> None:
        pass

    def validate(self) -> list[str]:
        return []


def test_config_domain_matches_required_domains():
    assert {d.name for d in ConfigDomain} == {
        'GLOBAL', 'MISSION', 'HARDWARE', 'SAFETY', 'LOGGING',
    }


def test_cannot_instantiate_abstract_configuration_provider():
    with pytest.raises(TypeError):
        IConfigurationProvider()


def test_fake_provider_returns_configured_value():
    provider = _FakeConfigProvider({
        ConfigDomain.SAFETY: {'max_altitude_m': 30},
    })
    assert provider.get(ConfigDomain.SAFETY, 'max_altitude_m') == 30


def test_fake_provider_falls_back_to_default():
    provider = _FakeConfigProvider({})
    assert provider.get(ConfigDomain.GLOBAL, 'missing_key', default='fallback') == 'fallback'


def test_fake_provider_validate_returns_empty_when_valid():
    provider = _FakeConfigProvider({})
    assert provider.validate() == []
