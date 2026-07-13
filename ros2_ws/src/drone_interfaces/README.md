# drone_interfaces

Shared interface contracts for DroneOS: abstract base classes, typed enums,
frozen dataclasses, and dependency-injection contracts. This package
contains **no runtime implementation** — every consumer of these contracts
(`drone_core`, `drone_utils`, `drone_dashboard`, and future mission
plugins) depends on `drone_interfaces` instead of on each other, so the
platform can substitute implementations (real or test doubles) without
touching consumer code.

## Why this package exists

DroneOS is built around dependency injection and interface segregation
(see `docs/architecture/software_architecture.md` and
`docs/phase0/coding_standards.md` in the repository root). Without a
neutral, dependency-free contracts package, every platform package would
need to import concrete classes from every other package, creating
circular dependencies and coupling mission code to platform internals.
`drone_interfaces` breaks that coupling: it depends on nothing but the
Python standard library, and every other package depends on it.

## What belongs here

- Lifecycle contract (`lifecycle.py`) shared by every managed component.
- Platform state machine contract and canonical transition table
  (`state_machine.py`).
- Configuration provider contract and domain enum (`configuration.py`).
- Centralized logger contract (`logging.py`).
- Health monitoring contract (`health.py`).
- Diagnostics publishing contract (`diagnostics.py`).
- Mission plugin and mission registry contracts (`mission.py`,
  `mission_registry.py`).
- Dependency-injection container contract (`di.py`).
- Shared exception hierarchy (`exceptions.py`).

## What does not belong here

Hardware-facing interfaces (camera, flight controller, rangefinder,
optical flow — documented at the architecture level in
`docs/interfaces/`) are intentionally **not** implemented in this
package. Phase 1 builds the DroneOS Core only; codifying hardware
contracts is deferred to the Hardware Abstraction Layer phase, per the
explicit Phase 1 exclusion list (no Camera, Pixhawk, MAVSDK, Optical
Flow, LiDAR, or Flight Control).

Similarly, `mission.py` defines only the plugin **contract** from
`docs/interfaces/mission_interface.md`. No concrete mission (e.g. QR
precision landing) is implemented here or anywhere in Phase 1.

## Package layout

```
drone_interfaces/
├── drone_interfaces/       # library source (ament_python convention)
│   ├── di.py
│   ├── configuration.py
│   ├── diagnostics.py
│   ├── exceptions.py
│   ├── health.py
│   ├── lifecycle.py
│   ├── logging.py
│   ├── mission.py
│   ├── mission_registry.py
│   └── state_machine.py
├── test/                   # unit tests + ament lint tests
├── docs/                   # architecture, public API, failure modes, testing guide
├── package.xml
├── setup.py
└── setup.cfg
```

## Build type: ament_python, not ament_cmake

This package has no C/C++ sources and defines no ROS interfaces (`.msg`
/ `.srv` / `.action`), so it uses the `ament_python` build type
(`setup.py` + `setup.cfg`) rather than `ament_cmake` +
`CMakeLists.txt`. `CMakeLists.txt` and `include/` are omitted because
they have no purpose in a pure-Python contracts package under ROS 2
Jazzy; forcing them in would be non-idiomatic and would add nothing.
`drone_msgs` (package 2) uses `ament_cmake` + `CMakeLists.txt` because it
generates code from `.msg`/`.srv`/`.action` definitions via `rosidl`.
`launch/` and `config/` are likewise omitted: this package defines no
nodes and has no runtime parameters to launch or configure.

## Dependencies

None beyond the Python standard library (`abc`, `dataclasses`, `enum`,
`typing`) at runtime. Test-only dependencies: `ament_copyright`,
`ament_flake8`, `ament_pep257`, `python3-pytest`. This package
deliberately does **not** depend on `rclpy` — interface contracts must
stay usable outside a ROS 2 process (e.g. in plain unit tests) per the
dependency-inversion principle in the coding standards.

## Usage

```python
from drone_interfaces.state_machine import IStateMachine, SystemState
from drone_interfaces.health import IHealthMonitor, HealthStatus

class BootStateMachine(IStateMachine):
    ...  # drone_core implements this
```

## Testing

```bash
colcon test --packages-select drone_interfaces
colcon test-result --verbose
```

See `docs/testing_guide.md` for what each test module covers.
