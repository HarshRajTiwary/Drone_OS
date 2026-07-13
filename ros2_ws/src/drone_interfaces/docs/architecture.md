# drone_interfaces — Architecture

## Position in the platform

`drone_interfaces` sits below every other DroneOS package. It has zero
intra-platform dependencies; every other Phase 1 package depends on it.

```
        drone_bringup, drone_dashboard, drone_core
                        |
                  drone_utils
                        |
                 drone_interfaces   (this package)
                        |
              Python standard library
```

`drone_msgs` is a sibling, not a dependent: it defines ROS wire types
(messages/services/actions) independently, using `rosidl`, not Python
ABCs. Where a component needs both a wire type and a typed Python
contract (e.g. a health monitor that both implements `IHealthMonitor`
and publishes a `drone_msgs/HealthReport`), the two are related only by
convention (matching field names), not by import — `drone_interfaces`
must never import generated message types, to keep it usable without a
ROS 2 runtime.

## Design rationale

Per `docs/architecture/software_architecture.md` (repository root), the
platform requires "explicit dependency injection rather than hidden
global state" and components that "receive interfaces, not concrete
device implementations." Concretely, that means:

1. `drone_core`'s Boot Manager constructs concrete implementations
   (`ConfigurationLoader`, `CentralLogger`, `HealthManager`, ...) but
   hands out only their `drone_interfaces` ABCs to everything else.
2. Tests substitute fakes (see this package's own `test/` directory for
   the pattern every downstream package should follow) by implementing
   the same ABC, never by monkeypatching a concrete class.
3. Because `drone_interfaces` has no ROS 2 dependency, every contract
   can be unit-tested with plain `pytest`, with no `rclpy` node, executor,
   or `ros2 run` required — this is what makes Phase 1's "Unit Tests"
   requirement (platform behavior independent of hardware) achievable.

## Contract groups

| Module | Contract(s) | Consumed by (future packages) |
| --- | --- | --- |
| `lifecycle.py` | `LifecycleComponent`, `LifecycleState` | `drone_core` Lifecycle Manager |
| `state_machine.py` | `IStateMachine`, `SystemState`, `VALID_TRANSITIONS` | `drone_core` State Manager, `drone_dashboard` |
| `configuration.py` | `IConfigurationProvider`, `ConfigDomain` | `drone_utils` Configuration Loader, all consumers |
| `logging.py` | `ILogger`, `LogLevel`, `LogRecord` | `drone_utils` Central Logger, all consumers |
| `health.py` | `IHealthMonitor`, `IHealthCheckable`, `HealthStatus` | `drone_core` Health Manager, `drone_dashboard` |
| `diagnostics.py` | `IDiagnosticsPublisher`, `DiagnosticLevel` | `drone_core` Diagnostics Publisher, `drone_dashboard` |
| `mission.py` | `IMissionPlugin`, `MissionState`, `MissionMetadata` | `drone_core` Mission Manager |
| `mission_registry.py` | `IMissionRegistry` | `drone_core` Mission Manager |
| `di.py` | `IServiceContainer` | `drone_core` Boot Manager |
| `exceptions.py` | `DroneOSError` hierarchy | every package |

## Why the state transition table lives here, not in drone_core

`VALID_TRANSITIONS` in `state_machine.py` is data, not behavior: it is
part of the *contract* (which transitions are legal is as much an
interface concern as the enum members themselves), so it has a single
source of truth that both `drone_core`'s implementation and any test
suite (including this package's own `test_state_machine.py`) can import
without depending on `drone_core`. `drone_core`'s State Manager owns the
*behavior* of applying that table (locking, observer notification,
history retention, persistence) — that is the implementation this
package deliberately excludes.
