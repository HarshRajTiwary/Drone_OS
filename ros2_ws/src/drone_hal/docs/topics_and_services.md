# drone_hal — Topics and Services

## Topics published

| Topic | Type | Rate | Published by |
| --- | --- | --- | --- |
| `/diagnostics` | `diagnostic_msgs/DiagnosticArray` | every `diagnostics_period_s` (default 1 Hz), only while the node is `ACTIVE` | `HardwareManagerNode` |

One `DiagnosticStatus` entry per **instantiated** device (a device that
has never been activated is not yet instantiated and does not appear).
`DiagnosticStatus.name` is the device id, `hardware_id` is the
descriptor's bus address, `level` follows
`drone_interfaces.diagnostics.DiagnosticLevel` (wire-compatible with
`DiagnosticStatus.OK/WARN/ERROR/STALE`), and `values` carries the
driver's `HealthReport.metrics` as string key/value pairs.

### Why `diagnostic_msgs`, not a `drone_hal`-specific message

`drone_msgs` (Phase 1, package 2) has not been built yet. `diagnostic_msgs`
is a standard ROS 2 package already installed and already exactly fits
this need, so using it avoids inventing a redundant message type and
avoids taking on a dependency on an unbuilt package. If `drone_msgs`
later defines a richer HAL-specific diagnostics message, this topic can
be extended or supplemented without breaking existing subscribers of
`/diagnostics` (a standard convention every ROS 2 tool already expects).

## Topics subscribed

None. `drone_hal` is a pure hardware-facing service; it has no upstream
ROS 2 dependency on any other DroneOS package's topics in Phase 2.

## Services

None in this package. Phase 2's `drone_hal` responsibilities (manager,
registry, loader, discovery, lifecycle, diagnostics, DI) are exercised
through the node's standard ROS 2 **lifecycle** service interface
(`~/change_state`, `~/get_state`, provided automatically by
`rclpy.lifecycle.LifecycleNode`), not through custom services. A
`/hal/list_devices`-style query service is a natural future addition
once `drone_msgs` exists to define its response type, but is not needed
by anything in Phase 2 and was not added speculatively.

## Actions

None.
