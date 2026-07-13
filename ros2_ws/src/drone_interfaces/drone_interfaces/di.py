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
Dependency-injection container contract used to wire platform services.

drone_core implements IServiceContainer once, at boot, and injects
interfaces (not concrete classes) into every managed component's
constructor. Tests substitute fakes by registering them against the same
interface types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar

T = TypeVar('T')


class IServiceContainer(ABC):
    """Contract for a typed dependency-injection container."""

    @abstractmethod
    def register(
        self,
        interface: type[T],
        factory: Callable[[], T],
        *,
        singleton: bool = True,
    ) -> None:
        """
        Register ``factory`` to satisfy requests for ``interface``.

        ``interface`` is the abstract type consumers will request; ``factory``
        is a zero-argument callable that produces an implementation. When
        ``singleton`` is True, ``factory`` is invoked once and the instance is
        cached; when False, a new instance is produced on every resolve.
        """

    @abstractmethod
    def resolve(self, interface: type[T]) -> T:
        """
        Return an implementation instance satisfying ``interface``.

        Raises DependencyResolutionError if no factory is registered for
        ``interface``.
        """

    @abstractmethod
    def has(self, interface: type[T]) -> bool:
        """Return True if a factory is registered for ``interface``."""
