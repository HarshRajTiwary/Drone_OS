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

"""Launch drone_core_node with its default configuration directory."""

from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    default_config_dir = os.path.join(get_package_share_directory('drone_core'), 'config')
    config_dir = LaunchConfiguration('config_dir')

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_dir',
            default_value=default_config_dir,
            description='Directory containing the 5 DroneOS config domain YAML files.',
        ),
        Node(
            package='drone_core',
            executable='drone_core_node',
            name='drone_core_node',
            parameters=[{'config_dir': config_dir}],
        ),
    ])
