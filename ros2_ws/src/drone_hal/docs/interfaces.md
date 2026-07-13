# drone_hal — Interfaces

## `drone_hal.device`

- `BusType` (Enum): `UART`, `SPI`, `I2C`, `CSI`, `USB`, `GPIO`.
- `DeviceConnectivity` (Enum): `UNKNOWN`, `PRESENT`, `MISSING`, `DISCONNECTED`.
- `DeviceDescriptor` (frozen dataclass): `device_id`, `device_type`,
  `bus`, `address`, `driver_class`, `metadata`.

## `drone_hal.driver`

- `IHardwareDriver(LifecycleComponent, IHealthCheckable)`: `descriptor`
  (property), `connectivity` (property), `reconnect()`, plus everything
  inherited from `LifecycleComponent` (`lifecycle_state`, `on_configure`,
  `on_activate`, `on_deactivate`, `on_cleanup`, `on_shutdown`,
  `on_error`) and `IHealthCheckable` (`check_health`).

## `drone_hal.camera_driver`

- `Frame` (frozen dataclass): `data`, `width`, `height`, `encoding`,
  `sequence`, `timestamp`.
- `ICameraDriver(IHardwareDriver)`: `capture() -> Frame`,
  `get_calibration() -> dict[str, float] | None`.

## `drone_hal.flight_controller_driver`

- `VehicleStatus`, `BatteryStatus`, `RCStatus` (frozen dataclasses).
- `IFlightControllerDriver(IHardwareDriver)`: `heartbeat_age_seconds()`,
  `get_vehicle_status()`, `get_battery_status()`, `get_rc_status()`.
  **No** `arm`, `disarm`, `takeoff`, `land`, `set_mode`, or
  `send_command` methods exist on this contract (enforced by
  `test_flight_controller_driver.py`).

## `drone_hal.rangefinder_driver`

- `DistanceMeasurement` (frozen dataclass): `distance_m`, `valid`,
  `signal_strength`, `sequence`, `timestamp`.
- `IRangefinderDriver(IHardwareDriver)`: `read_distance() -> DistanceMeasurement`.

## `drone_hal.optical_flow_driver`

- `FlowMeasurement` (frozen dataclass): `delta_x`, `delta_y`, `quality`,
  `sequence`, `timestamp`.
- `IOpticalFlowDriver(IHardwareDriver)`: `read_flow() -> FlowMeasurement`.

## `drone_hal.di`

- `ServiceContainer(IServiceContainer)`: concrete singleton/transient DI
  container. See `drone_interfaces.di` for the contract itself.

## `drone_hal.registry`

- `DriverFactory` — type alias for `Callable[[], IHardwareDriver]`.
- `IHardwareRegistry` (ABC): `register(descriptor, factory)`,
  `unregister(device_id)`, `get(device_id)`, `list_devices()`,
  `instantiated_devices()`.
- `HardwareRegistry(IHardwareRegistry)`: in-memory implementation with
  lazy instantiation and caching.

## `drone_hal.loader`

- `IDriverLoader` (ABC): `load(driver_class: str) -> type[IHardwareDriver]`.
- `DriverLoader(IDriverLoader)`: resolves `"module.path:ClassName"` via
  `importlib`.

## `drone_hal.discovery`

- `IDeviceDiscovery` (ABC): `scan(descriptors) -> dict[str, DeviceConnectivity]`.
- `DeviceDiscovery(IDeviceDiscovery)`: filesystem-presence-based
  implementation for UART/SPI/I2C/CSI bus types; returns `UNKNOWN` for
  USB and GPIO (no generic filesystem presence check applies).

## `drone_hal.manager`

- `DeviceOperationResult` (frozen dataclass): `device_id`, `success`, `detail`.
- `HardwareManager(LifecycleComponent)`: constructed with a registry,
  loader, discovery implementation, and a `list[DeviceDescriptor]`.
  `on_configure()` loads and registers every descriptor's driver;
  `on_activate()` / `on_deactivate()` / `on_shutdown()` fan out the
  matching lifecycle hook to every registered device, isolating
  per-device failures; `collect_diagnostics()` converts every
  instantiated driver's `check_health()` result to a `DiagnosticReport`;
  `rediscover()` re-runs bus presence scanning without changing
  lifecycle state.

## `drone_hal.node`

- `HardwareManagerNode(rclpy.lifecycle.LifecycleNode)`: the
  `hardware_manager_node` executable. Parameters: `devices_config_path`
  (string, path to a YAML file matching `config/hal_devices.yaml`'s
  shape), `diagnostics_period_s` (double, default `1.0`).

## `drone_hal.exceptions`

- `DeviceNotFoundError`, `DeviceAlreadyRegisteredError`,
  `DriverLoadError`, `DeviceDiscoveryError` — all subclass
  `drone_interfaces.exceptions.DroneOSError`.
