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

"""Unit tests for the rangefinder driver contract."""

from drone_hal.rangefinder_driver import DistanceMeasurement, IRangefinderDriver
import pytest


def test_cannot_instantiate_abstract_rangefinder_driver():
    with pytest.raises(TypeError):
        IRangefinderDriver()


def test_distance_measurement_fields():
    measurement = DistanceMeasurement(
        distance_m=1.23, valid=True, signal_strength=98.0, sequence=1, timestamp=0.0,
    )
    assert measurement.distance_m == 1.23
    assert measurement.valid is True
