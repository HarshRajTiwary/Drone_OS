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
Error-handling helpers implementing the escalation pattern.

From docs/phase0/error_handling_strategy.md: classify, log with
context, and re-raise as a DroneOSError rather than letting the
original exception type leak past a subsystem boundary.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from drone_interfaces.exceptions import DroneOSError
from drone_interfaces.logging import ILogger


@contextmanager
def error_boundary(
    logger: ILogger,
    subsystem: str,
    wrap_as: type[DroneOSError] = DroneOSError,
) -> Iterator[None]:
    """
    Catch any exception raised in the block, log it at ERROR, and re-raise.

    Exceptions already a DroneOSError pass through unwrapped so callers
    can still distinguish specific failure categories; anything else is
    wrapped in ``wrap_as`` with the original exception chained.
    """
    try:
        yield
    except DroneOSError as exc:
        logger.error(f'{subsystem} failed: {exc}')
        raise
    except Exception as exc:
        logger.error(f'{subsystem} failed: {exc}')
        raise wrap_as(f'{subsystem}: {exc}') from exc


def retry(times: int, exceptions: tuple[type[Exception], ...] = (Exception,)):
    """
    Return a decorator that retries a function up to ``times`` attempts.

    Only exceptions matching ``exceptions`` are retried; the last
    exception is re-raised if every attempt fails. ``times`` must be >= 1.
    """
    if times < 1:
        raise ValueError('times must be >= 1')

    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
            raise last_exc
        return wrapper
    return decorator
