# drone_hal — Architecture

## Position in the platform

```
        drone_camera   drone_fc   drone_rangefinder   drone_optical_flow   drone_gpio
              \            \             |                  /                /
               \____________\____________|_________________/________________/
                                          |
                                     drone_hal
                                    /          \
                       drone_interfaces        rclpy, diagnostic_msgs
```

`drone_hal` is the HAL's foundation package, analogous in role to
`drone_interfaces` for DroneOS Core: every hardware package depends on
it, it depends on nothing hardware-specific.

## Design rationale

Per the Phase 2 objective, "mission code must never communicate with
hardware directly... all hardware interaction must pass through the
HAL," and per the target-hardware section, DroneOS must support Pixhawk,
a Pi Camera, TFMini-S, and PMW3901 today, and unnamed future cameras,
flight controllers, and rangefinders tomorrow — "without changing
DroneOS Core or any mission plugin." That requirement drives every
design choice in this package:

1. **Dynamic driver loading, not static imports.** `DriverLoader`
   resolves a `"module:ClassName"` string from YAML at runtime. Adding a
   new camera driver package is a config change, not a `drone_hal` code
   change.
2. **Registry stores factories, not instances.** A device that is
   configured but never activated (or never physically present) never
   pays the cost of driver construction. This mirrors
   `IMissionRegistry`'s pattern from Phase 1.
3. **Presence is a separate axis from lifecycle state.** A driver can be
   `LifecycleState.ACTIVE` (successfully configured and running) while
   its `DeviceConnectivity` flips to `DISCONNECTED` mid-flight (a cable
   working loose). Collapsing these into one enum would make "device
   temporarily unreachable but otherwise fine" inexpressible.
4. **Per-device fault isolation in the manager's fan-out.**
   `HardwareManager._fan_out()` catches exceptions from one driver's
   lifecycle hook so a faulty rangefinder cannot prevent the camera or
   flight controller from activating. This directly implements
   `docs/phase0/error_handling_strategy.md`'s "graceful degradation
   where safe."

## Reused vs. new contracts

| Concern | Contract | Source | Why not reinvented |
| --- | --- | --- | --- |
| Lifecycle | `LifecycleComponent` | `drone_interfaces.lifecycle` (Phase 1) | Every device and `HardwareManager` itself follow the same initialize/configure/activate/deactivate/cleanup/shutdown state machine already defined and tested in Phase 1. |
| Health | `IHealthCheckable`, `HealthStatus` | `drone_interfaces.health` (Phase 1) | `check_health()` on a driver is exactly `IHealthCheckable.check_health()`; no new health vocabulary is needed. |
| Diagnostics | `DiagnosticReport`, `DiagnosticLevel` | `drone_interfaces.diagnostics` (Phase 1) | Wire-compatible with `diagnostic_msgs/DiagnosticStatus`, so `HardwareManager.collect_diagnostics()` converts directly with no new mapping table beyond `HealthStatus -> DiagnosticLevel`. |
| Dependency injection | `IServiceContainer` (contract), `ServiceContainer` (impl) | Contract from `drone_interfaces.di` (Phase 1); implementation added here | Phase 1 shipped the contract but no implementation (`drone_core` doesn't exist yet). `drone_hal` needs a working container now, so it provides one — see `docs/failure_modes.md` for what happens when `drone_core` eventually supersedes it. |
| Presence / connectivity | `DeviceConnectivity` | `drone_hal.device` (new) | Not covered by any Phase 1 contract; genuinely new to the HAL layer. |
| Bus type, device identity | `BusType`, `DeviceDescriptor` | `drone_hal.device` (new) | Hardware-specific by definition; Phase 1 explicitly deferred these to this phase. |

## Component responsibilities

| Component | Responsibility |
| --- | --- |
| `DeviceDescriptor` / `BusType` / `DeviceConnectivity` | Static device identity and dynamic physical presence. |
| `IHardwareDriver` and its `ICameraDriver` / `IFlightControllerDriver` / `IRangefinderDriver` / `IOpticalFlowDriver` extensions | The contract every concrete driver package implements. |
| `DriverLoader` | Resolves `driver_class` strings to importable types. |
| `HardwareRegistry` | Stores descriptors and factories; lazily instantiates and caches driver instances. |
| `DeviceDiscovery` | Bus-presence probing (file-existence checks only — protocol-level probing is each driver's job). |
| `ServiceContainer` | Generic typed DI container, usable by driver packages for their own internal wiring. |
| `HardwareManager` | Orchestrates the above; itself a `LifecycleComponent`; fans out lifecycle transitions across every registered device with fault isolation; converts health reports to diagnostics. |
| `HardwareManagerNode` | The ROS 2 `LifecycleNode` wrapper: loads YAML config, drives `HardwareManager` from ROS 2 lifecycle transitions, publishes `/diagnostics`. |

## What is explicitly excluded

Per the Phase 2 objective, this package (and this phase) does **not**
implement precision landing, QR detection, camera image processing, PID
control, flight-controller command logic, autonomous flight, search,
navigation, MAVSDK mission logic, AI, SLAM, or obstacle avoidance. Every
device-specific driver contract in this package (`ICameraDriver`, etc.)
is read/acquire-only — none define command or control methods.
