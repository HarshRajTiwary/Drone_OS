# drone_interfaces — Failure Modes

`drone_interfaces` executes no runtime logic, so it cannot itself fail at
runtime. Its failure modes are entirely about **contract violations** by
consumers, surfaced at two points:

## 1. Instantiation-time failures

Every interface in this package is an `abc.ABC` with `@abstractmethod`
members. Attempting to instantiate any interface directly, or a subclass
that has not implemented every abstract method, raises `TypeError` at
construction time (standard Python ABC behavior — see this package's
`test_*_interface.py` files, each of which asserts this for its
interface). This is intentional: a mission plugin or platform service
that only partially implements its contract must fail immediately at
startup, not at the first call to a missing method during flight.

## 2. Contract-defined exceptions

Downstream implementations are expected to raise the exceptions defined
in `exceptions.py` for the conditions documented on each ABC method's
docstring, for example:

| Exception | Raised by (per contract docstrings) | Condition |
| --- | --- | --- |
| `ConfigurationError` | `IConfigurationProvider.reload()` | reloaded configuration fails validation |
| `StateTransitionError` | `IStateMachine.transition()` | target state is not in `VALID_TRANSITIONS[current_state]` |
| `MissionError` | `IMissionRegistry.register/activate` | duplicate registration, unknown mission, or concurrent activation |
| `DependencyResolutionError` | `IServiceContainer.resolve()` | no factory registered for the requested interface |

`drone_interfaces` defines *when* these must be raised; it is each
implementing package's responsibility (and each implementing package's
own `failure_modes.md`) to describe recovery behavior.

## 3. Import-time failures

Because `drone_interfaces` depends only on the Python standard library,
the only import-time failure mode is a Python version mismatch (this
package targets Python 3.12 and uses PEP 604 union syntax and PEP 585
generics, e.g. `str | None`, `dict[str, Any]` — importing under Python
< 3.10 will raise `SyntaxError` at parse time, not a caught exception).

## Explicitly out of scope for this package

Hardware fault handling, sensor degradation, flight-safety fail-safes,
and mission-abort recovery are governed by
`docs/phase0/error_handling_strategy.md` and will be implemented by the
packages that own that behavior (`drone_core`'s Safety-adjacent
services in a later phase) — `drone_interfaces` only defines the shapes
those failures travel in (`HealthReport`, `DiagnosticReport`, the
`DroneOSError` hierarchy).
