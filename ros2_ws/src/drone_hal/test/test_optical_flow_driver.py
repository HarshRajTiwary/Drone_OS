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

"""Unit tests for the optical flow driver contract."""

from drone_hal.optical_flow_driver import FlowMeasurement, IOpticalFlowDriver
import pytest


def test_cannot_instantiate_abstract_optical_flow_driver():
    with pytest.raises(TypeError):
        IOpticalFlowDriver()


def test_flow_measurement_fields():
    measurement = FlowMeasurement(
        delta_x=0.5, delta_y=-0.2, quality=200.0, sequence=1, timestamp=0.0,
    )
    assert measurement.delta_x == 0.5
    assert measurement.quality == 200.0
