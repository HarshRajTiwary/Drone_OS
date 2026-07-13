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
Concrete dependency-injection container for DroneOS Core.

Same rationale as drone_hal.di.ServiceContainer: drone_interfaces defines
IServiceContainer but ships no implementation, and each top-level
package that needs DI now provides its own small one rather than
depending on a sibling package for it.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from drone_interfaces.di import IServiceContainer
from drone_interfaces.exceptions import DependencyResolutionError

T = TypeVar('T')


class ServiceContainer(IServiceContainer):
    """Minimal typed singleton/transient dependency-injection container."""

    def __init__(self) -> None:
        self._factories: dict[type, tuple[Callable[[], object], bool]] = {}
        self._singletons: dict[type, object] = {}

    def register(
        self,
        interface: type[T],
        factory: Callable[[], T],
        *,
        singleton: bool = True,
    ) -> None:
        self._factories[interface] = (factory, singleton)
        self._singletons.pop(interface, None)

    def resolve(self, interface: type[T]) -> T:
        if interface not in self._factories:
            raise DependencyResolutionError(
                f'no factory registered for {interface!r}',
            )
        factory, singleton = self._factories[interface]
        if not singleton:
            return factory()
        if interface not in self._singletons:
            self._singletons[interface] = factory()
        return self._singletons[interface]

    def has(self, interface: type[T]) -> bool:
        return interface in self._factories
