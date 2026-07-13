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

"""Unit tests for DriverLoader."""

from _fakes import FakeDriver
from drone_hal.exceptions import DriverLoadError
from drone_hal.loader import DriverLoader
import pytest


def test_load_valid_driver_class():
    loader = DriverLoader()
    driver_cls = loader.load('_fakes:FakeDriver')
    assert driver_cls is FakeDriver


def test_load_rejects_missing_colon():
    loader = DriverLoader()
    with pytest.raises(DriverLoadError):
        loader.load('_fakes.FakeDriver')


def test_load_rejects_unimportable_module():
    loader = DriverLoader()
    with pytest.raises(DriverLoadError):
        loader.load('no_such_module_xyz:Cls')


def test_load_rejects_missing_class():
    loader = DriverLoader()
    with pytest.raises(DriverLoadError):
        loader.load('_fakes:NoSuchClass')


def test_load_rejects_non_driver_class():
    loader = DriverLoader()
    with pytest.raises(DriverLoadError):
        loader.load('drone_hal.device:DeviceDescriptor')
