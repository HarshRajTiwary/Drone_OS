# drone_hal — Testing Guide

## Running the tests

```bash
cd ~/Drone_OS/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select drone_hal
colcon test --packages-select drone_hal
colcon test-result --verbose
```

## Test inventory

| Test file | Category | Covers |
| --- | --- | --- |
| `test_device.py` | Unit | `BusType`/`DeviceConnectivity` membership; `DeviceDescriptor` immutability and defaults. |
| `test_driver.py` | Unit + Hardware Mock | `IHardwareDriver` cannot be instantiated directly; `FakeDriver` (this package's mock hardware driver, in `_fakes.py`) walks the full lifecycle and reports health. |
| `test_camera_driver.py`, `test_flight_controller_driver.py`, `test_rangefinder_driver.py`, `test_optical_flow_driver.py` | Unit | Each device-specific ABC rejects direct instantiation; measurement/status dataclasses carry the right fields; `IFlightControllerDriver` is asserted to have **no** arm/takeoff/mode/command methods. |
| `test_di.py` | Unit | `ServiceContainer` singleton vs. transient resolution, re-registration, unresolved-interface error. |
| `test_registry.py` | Unit | Registration, duplicate rejection, lazy instantiation + caching, unregister. |
| `test_loader.py` | Driver | Dynamic loading of a valid driver class; rejection of malformed references, unimportable modules, missing classes, and non-`IHardwareDriver` classes. |
| `test_discovery.py` | Hardware Mock | Bus-presence scanning against real (via `tmp_path`) and absent filesystem paths; `UNKNOWN` for non-filesystem buses. |
| `test_manager.py` | Integration | Full configure→activate→deactivate→cleanup and configure→activate→shutdown walks across multiple mock devices; diagnostics collection reflects mock driver health; **fault isolation** — one device failing `on_activate()` does not block its sibling. |
| `test_hal_launch.py` | ROS Launch | `hardware_manager_node` starts under `ros2 launch`, logs its startup message, and exits cleanly on teardown. |
| `test_copyright.py`, `test_flake8.py`, `test_pep257.py` | Linter | License header, PEP 8, PEP 257 (`ament` standard). |

## The mock hardware pattern

`test/_fakes.py` defines `FakeDriver`, a complete `IHardwareDriver`
implementation with no real I/O — every hardware package built on top of
`drone_hal` should follow the same pattern (a `_fakes.py` implementing
its own `ICameraDriver`/`IFlightControllerDriver`/etc.) rather than
exercising real hardware in unit tests. `FakeDriver` supports injected
failure (`fail_on='on_activate'`) specifically so fault-isolation
behavior can be tested deterministically without needing a real device
to fail.

## What is intentionally not tested here

- Real device protocols (TFMini-S UART framing, PMW3901 SPI registers,
  MAVLink heartbeats, libcamera capture) — none of that code exists in
  this package; it belongs to Phase 2 packages 2-5, each of which is
  responsible for its own hardware-in-the-loop tests.
- Lifecycle *service* transitions driven externally via
  `ros2 lifecycle set` — `test_hal_launch.py` only proves the process
  starts and stops cleanly; the lifecycle state machine itself is
  proven without ROS in `test_manager.py`.
