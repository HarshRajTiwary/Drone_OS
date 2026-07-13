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

"""ROS launch test: drone_core_node starts cleanly and reaches READY."""

import unittest

from launch import LaunchDescription
from launch_ros.actions import Node
import launch_testing.actions
import launch_testing.asserts
import pytest


@pytest.mark.launch_test
def generate_test_description():
    core_node = Node(
        package='drone_core',
        executable='drone_core_node',
        name='drone_core_node',
    )
    return LaunchDescription([
        core_node,
        launch_testing.actions.ReadyToTest(),
    ])


class TestDroneCoreNodeReachesReady(unittest.TestCase):
    """Verifies the boot sequence completes and logs READY (rclpy logs to stderr)."""

    def test_logs_ready(self, proc_output):
        proc_output.assertWaitFor('drone_core READY', timeout=10, stream='stderr')


@launch_testing.post_shutdown_test()
class TestDroneCoreNodeShutdown(unittest.TestCase):
    """Verifies the node exits cleanly once the launch is torn down."""

    def test_exit_code(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
