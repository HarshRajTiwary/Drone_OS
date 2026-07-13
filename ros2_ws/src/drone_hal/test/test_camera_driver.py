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

"""Unit tests for the camera driver contract."""

from drone_hal.camera_driver import Frame, ICameraDriver
import pytest


def test_cannot_instantiate_abstract_camera_driver():
    with pytest.raises(TypeError):
        ICameraDriver()


def test_frame_is_frozen_and_carries_required_fields():
    frame = Frame(
        data=b'\x00\x01', width=640, height=480, encoding='rgb8',
        sequence=1, timestamp=0.0,
    )
    assert frame.width == 640
    assert frame.height == 480
    with pytest.raises(AttributeError):
        frame.sequence = 2
