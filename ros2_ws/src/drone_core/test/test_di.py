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

"""Unit tests for the concrete ServiceContainer."""

from drone_core.di import ServiceContainer
from drone_interfaces.exceptions import DependencyResolutionError
import pytest


class _Interface:
    """Stand-in interface type."""


class _Impl(_Interface):
    pass


def test_resolve_unregistered_interface_raises():
    with pytest.raises(DependencyResolutionError):
        ServiceContainer().resolve(_Interface)


def test_singleton_returns_same_instance():
    container = ServiceContainer()
    container.register(_Interface, _Impl, singleton=True)
    assert container.resolve(_Interface) is container.resolve(_Interface)


def test_non_singleton_returns_new_instance_each_time():
    container = ServiceContainer()
    container.register(_Interface, _Impl, singleton=False)
    assert container.resolve(_Interface) is not container.resolve(_Interface)


def test_has_reports_registration_state():
    container = ServiceContainer()
    assert container.has(_Interface) is False
    container.register(_Interface, _Impl)
    assert container.has(_Interface) is True
