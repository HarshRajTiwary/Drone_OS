# drone_core

DroneOS Core. Phase 1, package 4/6. Runs the boot sequence: config loads
-> logger starts -> health monitor starts -> mission manager starts ->
diagnostics start -> READY, waiting for a mission request.

## Modules

| Module | Implements |
| --- | --- |
| `state_machine.py` | `CoreStateMachine(IStateMachine)` against `drone_interfaces`' canonical transition table |
| `health_checks.py` | `CpuHealthCheck`, `RamHealthCheck`, `DiskHealthCheck`, `HeartbeatHealthCheck`, `RosGraphHealthCheck` (all `IHealthCheckable`) |
| `health_manager.py` | `CoreHealthMonitor(IHealthMonitor, LifecycleComponent)` |
| `mission_manager.py` | `CoreMissionRegistry(IMissionRegistry, LifecycleComponent)` — registration/discovery/activation only, no mission logic |
| `lifecycle_manager.py` | `LifecycleManager` — fault-isolated lifecycle fan-out (same pattern as `drone_hal.manager.HardwareManager`) |
| `boot_manager.py` | `BootManager` — the boot sequence itself, ROS-free and independently testable |
| `di.py` | `ServiceContainer(IServiceContainer)` |
| `node.py` | `DroneCoreNode` — the ROS 2 node: mission services, `/diagnostics` publisher |

## Why `DroneCoreNode` is a plain `Node`, not a `LifecycleNode`

The requested lifecycle (BOOTING -> INITIALIZING -> READY -> ...) is
already `CoreStateMachine`, driven by `BootManager` at construction time.
A `rclpy.lifecycle.LifecycleNode` on top would be a second, redundant
state machine with its own configure/activate callbacks mapping 1:1 onto
what `BootManager.boot()` already does — see `drone_hal` for where a
`LifecycleNode` *is* the right call (a device driver genuinely has no
other lifecycle authority).

## Topics / Services

- `/diagnostics` (`diagnostic_msgs/DiagnosticArray`) — health monitor output.
- `/drone_core/activate_mission`, `/drone_core/deactivate_mission`, `/drone_core/list_missions` (`drone_msgs` services) — thin wrappers over `CoreMissionRegistry`.

## Configuration

5 YAML files in `config/` (see `drone_utils`'s domain split):
`global_config.yaml`, `mission_config.yaml`, `hardware_config.yaml`,
`safety_config.yaml` (health check thresholds), `logging_config.yaml`.

## Dependencies

`drone_interfaces`, `drone_msgs`, `drone_utils`, `rclpy`, `diagnostic_msgs`.

## Testing

```bash
colcon test --packages-select drone_core
```
