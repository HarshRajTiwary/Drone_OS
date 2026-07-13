# drone_hal

DroneOS Hardware Abstraction Layer core: the hardware manager, device
registry, driver loader, device discovery, and the generic hardware
driver/device contracts that every concrete hardware package implements
against. Phase 2, package 1 of 8.

## Why this package exists

Mission code and DroneOS Core must never talk to hardware directly. Every
physical device (camera, flight controller, rangefinder, optical flow,
GPIO) is reached only through a driver that implements `IHardwareDriver`
(or one of its device-specific extensions defined here) and is registered
with the `HardwareManager`. `drone_hal` is what makes that possible: it is
the one package that knows how to load, register, discover, and drive the
lifecycle of *any* driver, without knowing anything about what a camera or
a flight controller actually is.

Concretely, `drone_hal` answers three questions the rest of the platform
should never have to:

1. **What hardware exists?** — `DeviceDescriptor` (from YAML) + `DeviceDiscovery` (bus presence).
2. **How do I get a driver instance for it?** — `DriverLoader` (dynamic import) + `HardwareRegistry` (lazy instantiation).
3. **How do I drive it safely?** — `HardwareManager` (lifecycle fan-out with per-device fault isolation).

## How it fits into DroneOS

```
        drone_camera, drone_fc, drone_rangefinder, drone_optical_flow, drone_gpio
                                        |
                                  drone_hal   (this package)
                                  /        \
                     drone_interfaces      rclpy / diagnostic_msgs
                     (Phase 1, package 1)
```

Device-specific packages (Phase 2, packages 2-6) depend on `drone_hal` to
implement `ICameraDriver`, `IFlightControllerDriver`,
`IRangefinderDriver`, `IOpticalFlowDriver`, or `IHardwareDriver` directly
(for GPIO). They are registered with the running `HardwareManager` purely
through a YAML entry (`config/hal_devices.yaml`) naming their driver
class — `drone_hal` never imports a device-specific package.

`drone_hal` reuses, rather than re-implements, two Phase 1 contracts:
`drone_interfaces.lifecycle.LifecycleComponent` for the
initialize/configure/activate/deactivate/cleanup/shutdown state machine
every device and the manager itself follow, and
`drone_interfaces.health.IHealthCheckable` for health reporting. This is
why `IHardwareDriver` in `driver.py` is a thin composition, not a new
state machine.

## Package layout

```
drone_hal/
├── drone_hal/
│   ├── device.py                    # BusType, DeviceConnectivity, DeviceDescriptor
│   ├── driver.py                     # IHardwareDriver (generic contract)
│   ├── camera_driver.py               # ICameraDriver, Frame
│   ├── flight_controller_driver.py     # IFlightControllerDriver, telemetry dataclasses
│   ├── rangefinder_driver.py            # IRangefinderDriver, DistanceMeasurement
│   ├── optical_flow_driver.py            # IOpticalFlowDriver, FlowMeasurement
│   ├── di.py                              # ServiceContainer (concrete IServiceContainer)
│   ├── registry.py                         # IHardwareRegistry, HardwareRegistry
│   ├── loader.py                            # IDriverLoader, DriverLoader
│   ├── discovery.py                          # IDeviceDiscovery, DeviceDiscovery
│   ├── manager.py                             # HardwareManager (orchestrator)
│   ├── node.py                                 # HardwareManagerNode (rclpy LifecycleNode)
│   └── exceptions.py                            # HAL-specific DroneOSError subclasses
├── launch/hal.launch.py
├── config/hal_devices.yaml
├── test/
└── docs/
```

## Build type: ament_python

Same rationale as `drone_interfaces`: no C/C++ sources, no `.msg`/`.srv`/
`.action` definitions, so `setup.py`/`setup.cfg` replace
`CMakeLists.txt`. `include/` is omitted for the same reason. `launch/`
and `config/` are present and real here, unlike `drone_interfaces`,
because this package does run a ROS 2 node.

## Dependencies

`rclpy`, `diagnostic_msgs`, `python3-yaml`, and `drone_interfaces`
(Phase 1, package 1). Deliberately **not** dependent on any
device-specific package (`drone_camera`, `drone_fc`, ...) — those depend
on `drone_hal`, never the other way around.

## Driver convention

Every driver class resolved by `DriverLoader` must accept exactly one
positional constructor argument, its `DeviceDescriptor`:
`DriverCls(descriptor)`. This is the only convention `drone_hal` imposes
on hardware packages.

## Usage

```bash
colcon build --packages-select drone_hal
source install/setup.bash
ros2 launch drone_hal hal.launch.py devices_config_path:=$(pwd)/src/drone_hal/config/hal_devices.yaml
```

With no devices configured, `hal_devices.yaml` ships an empty `devices:
[]` list — Phase 2 packages 2-6 do not exist yet — but the node,
registry, loader, and discovery machinery all run and are testable today.

## Testing

```bash
colcon test --packages-select drone_hal
colcon test-result --verbose
```

See `docs/testing_guide.md`.
