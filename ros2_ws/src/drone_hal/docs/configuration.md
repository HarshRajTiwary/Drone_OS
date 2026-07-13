# drone_hal — Configuration

## Node parameters

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `devices_config_path` | string | `''` (no devices) | Path to a YAML file listing device descriptors. |
| `diagnostics_period_s` | double | `1.0` | Interval between `/diagnostics` publishes while active. |

Set via `ros2 launch drone_hal hal.launch.py devices_config_path:=<path>`
or any standard ROS 2 parameter mechanism (YAML params file, `ros2 param
set`, etc.).

## Device descriptor file (`config/hal_devices.yaml`)

```yaml
devices:
  - device_id: tfmini_s_down       # unique across the whole HAL
    device_type: rangefinder        # free-form, informational
    bus: uart                        # one of: uart, spi, i2c, csi, usb, gpio
    address: /dev/ttyAMA0             # bus-specific: device node, spidev path, vid:pid, ...
    driver_class: "drone_rangefinder.driver:TFMiniDriver"  # module:ClassName
    metadata:                          # optional, driver-specific, string values only
      baudrate: "115200"
```

Every field is required except `metadata` (defaults to `{}`).
`driver_class` must resolve to a class implementing `IHardwareDriver`
(checked by `DriverLoader.load()` at configure time) and accepting a
single `DeviceDescriptor` constructor argument.

No devices are hardcoded anywhere in `drone_hal`'s source; the shipped
`config/hal_devices.yaml` defaults to `devices: []` because no
device-specific driver package exists yet in this repository.

## Per-device configuration

Device-specific tuning (camera FPS/resolution/exposure, rangefinder
frame rate, optical-flow rotation/scale, flight-controller baud rate and
heartbeat timeout, GPIO pin/mode/name maps — as listed in the Phase 2
brief) belongs in **each driver package's own** YAML config, loaded by
that driver during its own `on_configure()`. `drone_hal`'s
`hal_devices.yaml` only carries the fields needed to *find and load* a
driver (`device_id`, `bus`, `address`, `driver_class`); it deliberately
does not carry device-specific tuning fields, since `drone_hal` must
remain ignorant of what a camera or flight controller is. `metadata` is
the one exception: a small string-keyed bag for values a specific driver
needs at construction time (before its own config file is even read),
such as a baud rate needed to open the port. Drivers own their own
detailed config files.
