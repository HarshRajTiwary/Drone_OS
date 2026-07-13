# drone_interfaces — Public API

All symbols below are considered public API. Anything not listed
(leading-underscore names) is internal and may change without notice.

## `drone_interfaces.exceptions`

- `DroneOSError` — base of every platform exception.
- `ConfigurationError`, `ValidationError`, `LifecycleError`,
  `StateTransitionError`, `HealthCheckError`, `MissionError`,
  `DependencyResolutionError` — specific failure categories.

## `drone_interfaces.lifecycle`

- `LifecycleState` (Enum): `UNCONFIGURED`, `INACTIVE`, `ACTIVE`, `FINALIZED`.
- `LifecycleComponent` (ABC): `lifecycle_state` (property),
  `on_configure()`, `on_activate()`, `on_deactivate()`, `on_cleanup()`,
  `on_shutdown()`, `on_error(error)`.

## `drone_interfaces.state_machine`

- `SystemState` (Enum): `BOOTING`, `INITIALIZING`, `READY`,
  `MISSION_RUNNING`, `PAUSED`, `ERROR`, `SHUTDOWN`.
- `VALID_TRANSITIONS` (`dict[SystemState, frozenset[SystemState]]`) —
  canonical legal-transition table.
- `StateTransition` (frozen dataclass): `from_state`, `to_state`,
  `reason`, `timestamp`.
- `StateObserver` — type alias for `Callable[[StateTransition], None]`.
- `IStateMachine` (ABC): `current_state` (property),
  `can_transition(target)`, `transition(target, reason)`,
  `register_observer(observer)`, `history()`.

## `drone_interfaces.configuration`

- `ConfigDomain` (Enum): `GLOBAL`, `MISSION`, `HARDWARE`, `SAFETY`,
  `LOGGING`.
- `IConfigurationProvider` (ABC): `get(domain, key, default=None)`,
  `get_section(domain)`, `reload()`, `validate()`.

## `drone_interfaces.logging`

- `LogLevel` (IntEnum): `DEBUG=10`, `INFO=20`, `WARNING=30`,
  `ERROR=40`, `CRITICAL=50`.
- `LogRecord` (frozen dataclass): `timestamp`, `level`, `node_name`,
  `subsystem`, `message`, `correlation_id`, `context`.
- `ILogger` (ABC): `debug`, `info`, `warning`, `error`, `critical`
  (all `(message, **context)`), `with_subsystem(subsystem)`.

## `drone_interfaces.health`

- `HealthStatus` (Enum): `OK`, `DEGRADED`, `WARNING`, `CRITICAL`,
  `UNKNOWN`.
- `HealthReport` (frozen dataclass): `component`, `status`, `message`,
  `timestamp`, `metrics`.
- `IHealthCheckable` (ABC): `check_health()`.
- `IHealthMonitor` (ABC): `register(component)`,
  `unregister(component_name)`, `collect()`, `overall_status()`.

## `drone_interfaces.diagnostics`

- `DiagnosticLevel` (IntEnum, wire-compatible with
  `diagnostic_msgs/DiagnosticStatus`): `OK=0`, `WARN=1`, `ERROR=2`,
  `STALE=3`.
- `DiagnosticItem` (frozen dataclass): `key`, `value`.
- `DiagnosticReport` (frozen dataclass): `name`, `level`, `message`,
  `hardware_id`, `items`.
- `IDiagnosticsPublisher` (ABC): `publish(report)`,
  `publish_all(reports)`.

## `drone_interfaces.mission`

- `MissionState` (Enum): `UNINITIALIZED`, `INITIALIZED`, `RUNNING`,
  `PAUSED`, `COMPLETED`, `ABORTED`, `FAILED`.
- `MissionMetadata` (frozen dataclass): `name`, `version`,
  `description`, `author`.
- `IMissionPlugin` (ABC): `metadata` (property), `state` (property),
  `initialize(config)`, `start()`, `pause()`, `resume()`,
  `abort(reason)`, `shutdown()`, `diagnostics()`.

## `drone_interfaces.mission_registry`

- `MissionFactory` — type alias for `Callable[[], IMissionPlugin]`.
- `IMissionRegistry` (ABC): `register(factory, metadata)`,
  `discover()`, `activate(name, config)`, `deactivate(name)`,
  `active_mission()`, `mission_state(name)`.

## `drone_interfaces.di`

- `IServiceContainer` (ABC): `register(interface, factory, *,
  singleton=True)`, `resolve(interface)`, `has(interface)`.

## Stability

This is a Phase 1 baseline. Signatures may gain optional keyword
arguments in later phases but existing positional signatures and
return types should be treated as stable once `drone_core` (package 4)
implements against them.
