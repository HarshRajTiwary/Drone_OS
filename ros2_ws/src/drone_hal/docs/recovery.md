# drone_hal — Recovery

## Recovery primitives this package provides

- **Per-device isolation.** `HardwareManager._fan_out()` never lets one
  device's exception stop the fan-out loop, so a single faulty sensor
  cannot prevent the rest of the HAL from reaching `ACTIVE`. This is the
  primary recovery mechanism at this layer: containment, not retry.
- **`IHardwareDriver.reconnect()`.** A dedicated hook, separate from the
  lifecycle hooks, so a driver can attempt to re-establish communication
  without re-running its full `on_configure()` (which may do expensive
  or state-resetting work). `drone_hal` calls this contract into
  existence; it does not itself decide when to call it.
- **`HardwareManager.rediscover()`.** Re-runs bus-presence scanning
  without touching lifecycle state, so a caller (a future watchdog, or
  an operator via the dashboard) can check "is anything back yet?"
  cheaply and repeatedly.
- **Graceful shutdown fan-out.** `on_shutdown()` is fanned out the same
  fault-isolated way as `on_activate()`: a device that fails to shut
  down cleanly does not prevent its siblings from shutting down.

## What recovery policy is deferred, and to where

| Policy question | Deferred to |
| --- | --- |
| How often should a disconnected device be retried? | The driver package itself, or a future watchdog/health-monitor component that calls `reconnect()` / `rediscover()` on a schedule. |
| Should a mission abort if a device stays `CRITICAL`? | Safety / Mission Execution Engine (later phases) — `drone_hal` only makes the `CRITICAL` status observable via `/diagnostics`. |
| Should the whole platform enter a fail-safe state on repeated HAL faults? | Safety Supervisor (later phase), consuming `/diagnostics`. |

This split follows `docs/phase0/error_handling_strategy.md` directly:
"fail-safe behavior must be available independent of mission plugin
execution" — `drone_hal` supplies the primitives (isolation,
reconnect, rediscovery, diagnostics) that a safety-critical consumer
needs, without itself making safety-critical decisions.

## Manual recovery today

Until a watchdog component exists, an operator (or a test) can drive
recovery directly against a running `HardwareManager`:

```python
connectivity = manager.rediscover()
if connectivity['tfmini_s_down'] is DeviceConnectivity.PRESENT:
    driver = manager.registry.get('tfmini_s_down')
    driver.reconnect()
```
