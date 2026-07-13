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
Concrete IHealthCheckable implementations for CPU, RAM, disk, and heartbeat.

Stdlib-only (os.getloadavg, /proc/meminfo, shutil.disk_usage) so this
module has no third-party dependency beyond what ROS 2 Jazzy on Ubuntu
Server already guarantees.
"""

from __future__ import annotations

import os
import shutil
import time

from drone_interfaces.health import HealthReport, HealthStatus, IHealthCheckable
import rclpy


def _status_for_percent(
    percent: float, warn: float, degraded: float, critical: float,
) -> HealthStatus:
    if percent >= critical:
        return HealthStatus.CRITICAL
    if percent >= warn:
        return HealthStatus.WARNING
    if percent >= degraded:
        return HealthStatus.DEGRADED
    return HealthStatus.OK


class CpuHealthCheck(IHealthCheckable):
    """Reports 1-minute load average as a percentage of available CPUs."""

    def __init__(
        self, degraded_percent: float = 70.0, warn_percent: float = 85.0,
        critical_percent: float = 95.0,
    ) -> None:
        self._degraded = degraded_percent
        self._warn = warn_percent
        self._critical = critical_percent

    def check_health(self) -> HealthReport:
        cpu_count = os.cpu_count() or 1
        load_1min = os.getloadavg()[0]
        percent = min(100.0, (load_1min / cpu_count) * 100.0)
        status = _status_for_percent(percent, self._warn, self._degraded, self._critical)
        return HealthReport(
            component='cpu', status=status,
            message=f'load {load_1min:.2f} over {cpu_count} cpu(s)',
            timestamp=time.time(),
            metrics={
                'load_1min': load_1min, 'cpu_count': float(cpu_count), 'load_percent': percent,
            },
        )


class RamHealthCheck(IHealthCheckable):
    """Reports memory usage percentage from /proc/meminfo."""

    def __init__(
        self, degraded_percent: float = 70.0, warn_percent: float = 85.0,
        critical_percent: float = 95.0,
    ) -> None:
        self._degraded = degraded_percent
        self._warn = warn_percent
        self._critical = critical_percent

    def check_health(self) -> HealthReport:
        meminfo = self._read_meminfo()
        total = meminfo.get('MemTotal', 1)
        available = meminfo.get('MemAvailable', 0)
        used_percent = ((total - available) / total) * 100.0 if total else 0.0
        status = _status_for_percent(used_percent, self._warn, self._degraded, self._critical)
        return HealthReport(
            component='ram', status=status,
            message=f'{used_percent:.1f}% used',
            timestamp=time.time(),
            metrics={'used_percent': used_percent, 'total_kb': float(total)},
        )

    @staticmethod
    def _read_meminfo() -> dict[str, int]:
        values: dict[str, int] = {}
        try:
            with open('/proc/meminfo', encoding='utf-8') as handle:
                for line in handle:
                    key, _, rest = line.partition(':')
                    digits = ''.join(ch for ch in rest if ch.isdigit())
                    if digits:
                        values[key] = int(digits)
        except OSError:
            return {}
        return values


class DiskHealthCheck(IHealthCheckable):
    """Reports disk usage percentage for a given mount path (default '/')."""

    def __init__(
        self, path: str = '/', degraded_percent: float = 70.0,
        warn_percent: float = 85.0, critical_percent: float = 95.0,
    ) -> None:
        self._path = path
        self._degraded = degraded_percent
        self._warn = warn_percent
        self._critical = critical_percent

    def check_health(self) -> HealthReport:
        usage = shutil.disk_usage(self._path)
        used_percent = (usage.used / usage.total) * 100.0 if usage.total else 0.0
        status = _status_for_percent(used_percent, self._warn, self._degraded, self._critical)
        return HealthReport(
            component='disk', status=status,
            message=f'{used_percent:.1f}% used on {self._path}',
            timestamp=time.time(),
            metrics={'used_percent': used_percent, 'total_bytes': float(usage.total)},
        )


class HeartbeatHealthCheck(IHealthCheckable):
    """Reports CRITICAL if beat() has not been called within stale_after_s."""

    def __init__(self, stale_after_s: float = 5.0) -> None:
        self._stale_after_s = stale_after_s
        self._last_beat = time.time()

    def beat(self) -> None:
        """Record a liveness signal, resetting the staleness clock."""
        self._last_beat = time.time()

    def check_health(self) -> HealthReport:
        age = time.time() - self._last_beat
        status = HealthStatus.CRITICAL if age > self._stale_after_s else HealthStatus.OK
        return HealthReport(
            component='heartbeat', status=status,
            message=f'last beat {age:.2f}s ago',
            timestamp=time.time(),
            metrics={'age_s': age},
        )


class RosGraphHealthCheck(IHealthCheckable):
    """Reports node/ROS-graph status by wrapping an rclpy node, when available."""

    def __init__(self, ros_node=None) -> None:
        self._ros_node = ros_node

    def check_health(self) -> HealthReport:
        if self._ros_node is None:
            return HealthReport(
                component='ros_graph', status=HealthStatus.UNKNOWN,
                message='no ROS node bound', timestamp=time.time(),
            )
        ok = rclpy.ok() and self._ros_node.context.ok()
        status = HealthStatus.OK if ok else HealthStatus.CRITICAL
        return HealthReport(
            component='ros_graph', status=status,
            message='rclpy context ok' if ok else 'rclpy context not ok',
            timestamp=time.time(),
        )
