# drone_bringup

System startup for DroneOS. Phase 1, package 5/6. No node logic of its
own — launch files, parameter loading, and node startup order only.

## Contents

| Path | Purpose |
| --- | --- |
| `launch/droneos.launch.py` | Full system: `drone_hal` then `drone_core`, sequenced via `OnProcessStart` |
| `drone_bringup/startup_order.py` | The same order expressed as data (`STARTUP_ORDER`), independently unit-tested |
| `config/*.yaml` | The deployed instance of DroneOS Core's 5 config domains (distinct from `drone_core`'s package-internal defaults, which exist only for that package's own tests) |

## Why event-handler sequencing, not just declaration order

Listing two `Node` actions in a `LaunchDescription` starts them
concurrently — ROS 2 launch does not serialize by list position. Real
node startup order (hardware discovery before Core declares READY)
requires `RegisterEventHandler(OnProcessStart(...))`, which is what
`droneos.launch.py` uses. `startup_order.py` is the single source of
truth for what that order should be; the launch file's event handler
implements it.

## Usage

```bash
ros2 launch drone_bringup droneos.launch.py
```

Override either config location:

```bash
ros2 launch drone_bringup droneos.launch.py \
  core_config_dir:=/etc/droneos/config \
  devices_config_path:=/etc/droneos/hal_devices.yaml
```

## Dependencies

`drone_core`, `drone_hal`, `launch`, `launch_ros`.

## Testing

```bash
colcon test --packages-select drone_bringup
```

`test_startup_order.py` checks the ordering data is internally
consistent (no forward dependencies); `test_droneos_launch.py` actually
launches both nodes and confirms `drone_hal` starts before `drone_core`
reaches READY.
