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
BootManager: drives the Phase 1 boot sequence end to end.

Configuration loads -> Logger starts -> Health Monitor starts -> Mission
Manager starts -> Diagnostics start -> READY, waiting for a mission
request. Pure Python, constructible and fully testable without rclpy;
node.py wraps this in an rclpy LifecycleNode and adds the ROS-graph
health check and topic/service surface.
"""

from __future__ import annotations

from drone_core.health_manager import CoreHealthMonitor
from drone_core.lifecycle_manager import LifecycleManager
from drone_core.mission_manager import CoreMissionRegistry
from drone_core.state_machine import CoreStateMachine
from drone_interfaces.configuration import ConfigDomain
from drone_interfaces.state_machine import SystemState
from drone_utils.config_loader import YamlConfigurationProvider
from drone_utils.logger import CentralLogger


class BootManager:
    """Owns configuration, logging, state, health, and mission services for one boot."""

    def __init__(self, config_dir: str, node_name: str = 'drone_core') -> None:
        self.config = YamlConfigurationProvider(config_dir)
        self.logger = CentralLogger(node_name)
        self.state_machine = CoreStateMachine()
        self.health_monitor = CoreHealthMonitor(self.config.get_section(ConfigDomain.SAFETY))
        self.mission_registry = CoreMissionRegistry()
        self.lifecycle_manager = LifecycleManager({
            'health_monitor': self.health_monitor,
            'mission_manager': self.mission_registry,
        })

    def boot(self) -> bool:
        """Run BOOTING -> INITIALIZING -> READY (or -> ERROR on failure)."""
        self.logger.info('boot sequence starting')
        self.state_machine.transition(SystemState.INITIALIZING, 'configuration loaded')
        self.logger.info('logger started')

        if not self.lifecycle_manager.on_configure():
            self.state_machine.transition(SystemState.ERROR, 'lifecycle configure failed')
            self.logger.error('boot failed during configure')
            return False
        self.logger.info('health monitor and mission manager configured')

        if not self.lifecycle_manager.on_activate():
            self.state_machine.transition(SystemState.ERROR, 'lifecycle activate failed')
            self.logger.error('boot failed during activate')
            return False
        self.logger.info('health monitor and mission manager active; diagnostics ready')

        self.state_machine.transition(SystemState.READY, 'boot sequence complete')
        self.logger.info('DroneOS READY, waiting for mission request')
        return True

    def shutdown(self) -> bool:
        """Deactivate and shut down every managed service, then transition to SHUTDOWN."""
        ok = self.lifecycle_manager.on_deactivate() and self.lifecycle_manager.on_shutdown()
        self.state_machine.transition(SystemState.SHUTDOWN, 'shutdown requested')
        self.logger.info('DroneOS shutdown complete')
        return ok
