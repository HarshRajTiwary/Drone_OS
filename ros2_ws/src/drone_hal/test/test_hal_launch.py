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
ROS launch test: hardware_manager_node starts cleanly under ros2 launch.

Deeper lifecycle-transition behavior (configure -> activate -> ... ->
shutdown fan-out across devices) is already covered without any ROS
dependency by test_manager.py; this test only proves the executable,
entry point, and package data files are wired correctly end-to-end,
which pure-Python unit tests cannot catch.
"""

import unittest

from launch import LaunchDescription
from launch_ros.actions import Node
import launch_testing.actions
import launch_testing.asserts
import pytest


@pytest.mark.launch_test
def generate_test_description():
    hal_node = Node(
        package='drone_hal',
        executable='hardware_manager_node',
        name='hardware_manager_node',
    )
    return LaunchDescription([
        hal_node,
        launch_testing.actions.ReadyToTest(),
    ])


class TestHardwareManagerNodeStartsCleanly(unittest.TestCase):
    """Verifies the node logs its startup message (rclpy logs to stderr by default)."""

    def test_logs_startup_message(self, proc_output):
        proc_output.assertWaitFor(
            'drone_hal hardware_manager_node started', timeout=10, stream='stderr',
        )


@launch_testing.post_shutdown_test()
class TestHardwareManagerNodeShutdown(unittest.TestCase):
    """Verifies the node exits cleanly once the launch is torn down."""

    def test_exit_code(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
