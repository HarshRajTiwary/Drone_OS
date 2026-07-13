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
Canonical DroneOS node startup order, expressed as data.

Kept independent of launch-file control flow so the intended order is
independently testable and documented in one place.
droneos.launch.py sequences nodes using this exact list.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StartupStage:
    """One node's position in the DroneOS startup sequence."""

    node_name: str
    package: str
    depends_on: tuple[str, ...] = ()


#: Hardware manager starts first so device discovery has run before core
#: declares READY; drone_core does not hard-depend on it at import time,
#: but this is the operationally correct order for a real deployment.
STARTUP_ORDER: tuple[StartupStage, ...] = (
    StartupStage('hardware_manager_node', 'drone_hal'),
    StartupStage('drone_core_node', 'drone_core', depends_on=('hardware_manager_node',)),
)


def node_names_in_order() -> tuple[str, ...]:
    """Return node names in the order they should be started."""
    return tuple(stage.node_name for stage in STARTUP_ORDER)
