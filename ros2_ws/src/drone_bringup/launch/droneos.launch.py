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
Full DroneOS system startup: drone_hal then drone_core, in that order.

Node startup order is enforced with an OnProcessStart event handler
rather than left to launch's default (roughly concurrent) scheduling, so
hardware discovery has begun before Core declares READY. See
drone_bringup/startup_order.py for the same order expressed as data.
"""

from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node


def generate_launch_description() -> LaunchDescription:
    default_devices_config = os.path.join(
        get_package_share_directory('drone_hal'), 'config', 'hal_devices.yaml',
    )
    default_core_config_dir = os.path.join(
        get_package_share_directory('drone_bringup'), 'config',
    )
    devices_config_path = LaunchConfiguration('devices_config_path')
    core_config_dir = LaunchConfiguration('core_config_dir')

    hal_node = LifecycleNode(
        package='drone_hal',
        executable='hardware_manager_node',
        name='hardware_manager_node',
        namespace='',
        parameters=[{'devices_config_path': devices_config_path}],
    )
    core_node = Node(
        package='drone_core',
        executable='drone_core_node',
        name='drone_core_node',
        parameters=[{'config_dir': core_config_dir}],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'devices_config_path', default_value=default_devices_config,
            description='Path to the HAL device descriptor YAML file.',
        ),
        DeclareLaunchArgument(
            'core_config_dir', default_value=default_core_config_dir,
            description='Directory containing the 5 DroneOS config domain YAML files.',
        ),
        hal_node,
        RegisterEventHandler(
            OnProcessStart(target_action=hal_node, on_start=[core_node]),
        ),
    ])
