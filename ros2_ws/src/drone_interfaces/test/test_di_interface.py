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

"""Unit tests for the dependency-injection container contract."""

from drone_interfaces.di import IServiceContainer
from drone_interfaces.exceptions import DependencyResolutionError
import pytest


class _ILogger:
    """Stand-in interface type for container tests."""


class _ConsoleLogger(_ILogger):
    pass


class _FakeContainer(IServiceContainer):
    def __init__(self) -> None:
        self._factories: dict[type, tuple] = {}
        self._singletons: dict[type, object] = {}

    def register(self, interface, factory, *, singleton=True):
        self._factories[interface] = (factory, singleton)

    def resolve(self, interface):
        if interface not in self._factories:
            raise DependencyResolutionError(f'no factory registered for {interface}')
        factory, singleton = self._factories[interface]
        if not singleton:
            return factory()
        if interface not in self._singletons:
            self._singletons[interface] = factory()
        return self._singletons[interface]

    def has(self, interface):
        return interface in self._factories


def test_cannot_instantiate_abstract_container():
    with pytest.raises(TypeError):
        IServiceContainer()


def test_resolve_unregistered_interface_raises():
    container = _FakeContainer()
    with pytest.raises(DependencyResolutionError):
        container.resolve(_ILogger)


def test_singleton_resolve_returns_same_instance():
    container = _FakeContainer()
    container.register(_ILogger, _ConsoleLogger, singleton=True)
    first = container.resolve(_ILogger)
    second = container.resolve(_ILogger)
    assert first is second


def test_non_singleton_resolve_returns_new_instance_each_time():
    container = _FakeContainer()
    container.register(_ILogger, _ConsoleLogger, singleton=False)
    first = container.resolve(_ILogger)
    second = container.resolve(_ILogger)
    assert first is not second


def test_has_reports_registration_state():
    container = _FakeContainer()
    assert container.has(_ILogger) is False
    container.register(_ILogger, _ConsoleLogger)
    assert container.has(_ILogger) is True
