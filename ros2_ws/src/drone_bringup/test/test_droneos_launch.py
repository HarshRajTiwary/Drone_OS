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
ROS launch test for droneos.launch.py.

Brings up drone_hal then drone_core, in that order, and confirms
drone_core reaches READY.
"""

import os
import unittest

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_testing.actions
import launch_testing.asserts
import pytest


@pytest.mark.launch_test
def generate_test_description():
    launch_file = os.path.join(
        get_package_share_directory('drone_bringup'), 'launch', 'droneos.launch.py',
    )
    bringup = IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file))
    return LaunchDescription([
        bringup,
        launch_testing.actions.ReadyToTest(),
    ])


class TestDroneOsSystemStartsInOrder(unittest.TestCase):
    """Verifies both nodes start and drone_core reaches READY after drone_hal."""

    def test_hal_starts_then_core_reaches_ready(self, proc_output):
        proc_output.assertWaitFor(
            'drone_hal hardware_manager_node started', timeout=15, stream='stderr',
        )
        proc_output.assertWaitFor('drone_core READY', timeout=15, stream='stderr')


@launch_testing.post_shutdown_test()
class TestDroneOsSystemShutdown(unittest.TestCase):
    """Verifies both processes exit cleanly once the launch is torn down."""

    def test_exit_codes(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
