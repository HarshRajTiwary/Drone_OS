# drone_hal — Failure Modes

Categorized per `docs/phase0/error_handling_strategy.md`'s taxonomy.

## Hardware errors

| Condition | Detection | Behavior |
| --- | --- | --- |
| Device missing at configure time | `DeviceDiscovery.scan()` returns `DeviceConnectivity.MISSING` for that descriptor's address | Recorded, not fatal: `HardwareManager.on_configure()` still succeeds so healthy devices are unaffected. The missing device's own driver will typically fail its `on_activate()` (see below) once the manager tries to activate it. |
| Device present but driver activation fails | Exception raised from a driver's `on_activate()` during `HardwareManager._fan_out()` | Caught per-device: the failing driver's `on_error(exc)` is invoked, its `DeviceOperationResult.success` is `False`, and the fan-out continues to every other device. `HardwareManager.on_activate()` returns `False` overall so the node's `on_activate` transition fails and the caller is told loudly — but siblings still transitioned successfully. |
| Device disconnects mid-flight | Not yet detected automatically by `drone_hal` in Phase 2 — a device's own `check_health()` or `read_*()` calls (implemented by its driver package) are expected to surface this as a `HealthStatus.CRITICAL` report or a raised exception. `HardwareManager.rediscover()` can be called (e.g. from a future watchdog) to refresh `DeviceConnectivity` on demand. | Reconnection is `IHardwareDriver.reconnect()` — a driver-specific operation `drone_hal` defines the contract for but does not itself schedule or retry; that policy (when/how often to retry) belongs to whichever component drives reconnection (a later phase or the driver itself). |

## Software errors

| Condition | Detection | Behavior |
| --- | --- | --- |
| `driver_class` string malformed, unimportable, missing, or not an `IHardwareDriver` subclass | `DriverLoader.load()` | Raises `DriverLoadError` during `HardwareManager.on_configure()`, which propagates out of `on_configure()` (fails loudly at startup rather than silently skipping a misconfigured device). |
| Duplicate `device_id` in YAML | `HardwareRegistry.register()` | Raises `DeviceAlreadyRegisteredError`, propagates the same way. |
| Query for an unregistered/unknown device id | `HardwareRegistry.get()` | Raises `DeviceNotFoundError`. |

## Diagnostics and observability

Every device's `check_health()` result is converted to a
`DiagnosticReport` and published on `/diagnostics` while the node is
active (see `docs/topics_and_services.md`), independent of whether that
device is currently healthy — a `CRITICAL` report is exactly as visible
as an `OK` one; nothing is suppressed.

## Explicitly out of scope for drone_hal

Automatic reconnection *scheduling*, exponential backoff policy, and
mission-level abort/hold decisions in response to a hardware fault are
not implemented here — per the Phase 2 objective, `drone_hal` provides
the mechanism (lifecycle, health, diagnostics, `reconnect()`) and later
phases (Flight Core, Safety) decide policy on top of it.
