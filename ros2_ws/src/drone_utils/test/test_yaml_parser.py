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

"""Unit tests for yaml_parser."""

from drone_interfaces.exceptions import ConfigurationError
from drone_utils.yaml_parser import dump_yaml_file, get_dotted, load_yaml_file
import pytest


def test_load_missing_file_returns_empty_dict(tmp_path):
    assert load_yaml_file(tmp_path / 'missing.yaml') == {}


def test_load_and_dump_round_trip(tmp_path):
    path = tmp_path / 'config.yaml'
    dump_yaml_file(path, {'safety': {'max_altitude_m': 30}})
    assert load_yaml_file(path) == {'safety': {'max_altitude_m': 30}}


def test_load_rejects_non_mapping_top_level(tmp_path):
    path = tmp_path / 'list.yaml'
    path.write_text('- a\n- b\n')
    with pytest.raises(ConfigurationError):
        load_yaml_file(path)


def test_load_rejects_invalid_yaml(tmp_path):
    path = tmp_path / 'broken.yaml'
    path.write_text('key: [unclosed')
    with pytest.raises(ConfigurationError):
        load_yaml_file(path)


def test_get_dotted_traverses_nested_keys():
    data = {'safety': {'limits': {'max_altitude_m': 30}}}
    assert get_dotted(data, 'safety.limits.max_altitude_m') == 30


def test_get_dotted_returns_default_when_missing():
    assert get_dotted({}, 'a.b.c', default='fallback') == 'fallback'
