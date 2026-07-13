# drone_core — Failure Modes

| Condition | Behavior |
| --- | --- |
| `lifecycle_manager.on_configure()` fails (a component raises) | Faulty component isolated (`on_error` invoked); `BootManager.boot()` transitions to `SystemState.ERROR` and returns `False`. Boot does not proceed to READY. |
| `lifecycle_manager.on_activate()` fails | Same as above, at the activate stage. |
| Malformed YAML in any config domain | `ConfigurationError` from `YamlConfigurationProvider`, raised out of `BootManager.__init__` — the node fails to construct rather than boot into a half-configured state. |
| `ActivateMission` requested for an unknown or already-active mission | `MissionError` caught in `DroneCoreNode._on_activate`, returned as `response.success=False` with the error message — the service never raises past the node. |
| CPU/RAM/disk past `critical_percent` | `HealthReport.status = CRITICAL`, surfaced on `/diagnostics` at `DiagnosticLevel.ERROR`. `drone_core` does not itself abort or fail-safe on this — that is a later phase's Safety Supervisor, consuming `/diagnostics`. |
| Heartbeat stale (`age_s > stale_after_s`) | `HealthStatus.CRITICAL`; the node's own diagnostics timer calls `heartbeat.beat()` on every publish, so staleness only occurs if the node's executor itself stalls. |

No automatic reconnection or recovery beyond fault isolation is
implemented here, matching `docs/phase0/error_handling_strategy.md`'s
split between platform-level containment and safety-level policy.
