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

"""Unit tests for the canonical startup order data."""

from drone_bringup.startup_order import node_names_in_order, STARTUP_ORDER


def test_hardware_manager_starts_before_drone_core():
    names = node_names_in_order()
    assert names.index('hardware_manager_node') < names.index('drone_core_node')


def test_drone_core_depends_on_hardware_manager():
    core_stage = next(s for s in STARTUP_ORDER if s.node_name == 'drone_core_node')
    assert 'hardware_manager_node' in core_stage.depends_on


def test_every_dependency_is_itself_a_listed_stage():
    names = {s.node_name for s in STARTUP_ORDER}
    for stage in STARTUP_ORDER:
        assert set(stage.depends_on) <= names


def test_no_stage_depends_on_a_later_stage():
    names = node_names_in_order()
    for index, stage in enumerate(STARTUP_ORDER):
        for dependency in stage.depends_on:
            assert names.index(dependency) < index
