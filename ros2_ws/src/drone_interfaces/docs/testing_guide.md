# drone_interfaces — Testing Guide

## Running the tests

```bash
cd ~/Drone_OS/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select drone_interfaces
colcon test --packages-select drone_interfaces
colcon test-result --verbose
```

Or, without colcon, directly with pytest against the installed package:

```bash
source ~/Drone_OS/ros2_ws/install/setup.bash
python3 -m pytest src/drone_interfaces/test -v
```

## What each test module covers

| Test file | Covers |
| --- | --- |
| `test_exceptions.py` | Every exception subclasses `DroneOSError`; message propagation. |
| `test_lifecycle.py` | `LifecycleComponent` cannot be instantiated directly; a full concrete lifecycle walk (unconfigured → inactive → active → inactive → unconfigured → finalized). |
| `test_state_machine.py` | `SystemState` has exactly the seven required members; every state has a `VALID_TRANSITIONS` entry; `SHUTDOWN` is terminal; every non-terminal state can reach `SHUTDOWN` (fail-safe reachability check); `StateTransition` is immutable. |
| `test_configuration_interface.py` | `ConfigDomain` has exactly the five required members; a fake provider satisfies `get`/`get_section`/`reload`/`validate`. |
| `test_logging_interface.py` | `LogLevel` has exactly the five required severities in monotonic order; a fake logger records at the correct level; `with_subsystem` returns a bound logger; `LogRecord` is immutable. |
| `test_health_interface.py` | A fake monitor aggregates `IHealthCheckable` reports; `overall_status()` degrades correctly with no components registered. |
| `test_diagnostics_interface.py` | `DiagnosticLevel` values match `diagnostic_msgs/DiagnosticStatus` wire values exactly; single and batch publish. |
| `test_mission_interface.py` | Full mission lifecycle through a fake plugin; registry rejects duplicate registration, unknown-mission activation, and concurrent activation (mirrors `docs/interfaces/mission_interface.md`). |
| `test_di_interface.py` | Singleton vs. non-singleton resolution semantics; unresolved interface raises `DependencyResolutionError`. |
| `test_copyright.py`, `test_flake8.py`, `test_pep257.py` | Standard `ament` linters: license header, PEP 8 (via flake8), and PEP 257 docstring conventions. |

## Testing pattern for downstream packages

Every test above follows the same shape used across DroneOS: define a
minimal concrete subclass (`_FakeX`) inside the test file that satisfies
the ABC, then assert both (a) the ABC rejects direct instantiation and
(b) the fake behaves as the contract's docstrings specify. `drone_core`
and later packages should reuse this pattern rather than importing real
implementations into unit tests — real implementations belong in
integration tests once hardware- or ROS-dependent packages exist.

## What is intentionally not tested here

- ROS 2 topic/service/action wiring — this package has no nodes.
- Launch tests — this package has no launch files (see package
  `README.md` for why).
- Hardware and simulation tests — out of scope until the HAL and
  Simulation layers are implemented in a later phase.
