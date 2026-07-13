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

"""Launch the HAL hardware_manager_node with its default device configuration."""

from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode


def generate_launch_description() -> LaunchDescription:
    default_config = os.path.join(
        get_package_share_directory('drone_hal'), 'config', 'hal_devices.yaml',
    )
    devices_config_path = LaunchConfiguration('devices_config_path')

    return LaunchDescription([
        DeclareLaunchArgument(
            'devices_config_path',
            default_value=default_config,
            description='Path to the HAL device descriptor YAML file.',
        ),
        LifecycleNode(
            package='drone_hal',
            executable='hardware_manager_node',
            name='hardware_manager_node',
            namespace='',
            parameters=[{'devices_config_path': devices_config_path}],
        ),
    ])
