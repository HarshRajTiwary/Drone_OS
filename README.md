# DroneOS

A modular, mission-agnostic autonomous flight platform for a Raspberry Pi 4
companion computer, Pixhawk 2.4.8 (ArduPilot) flight controller, and ROS 2
Jazzy on Ubuntu Server 24.04 LTS. See [docs/README.md](docs/README.md) for
the full architecture, requirements, and engineering standards baseline.

Initial mission target: GPS-denied QR precision landing. The platform is
built so future missions (AI target following, inspection, mapping,
delivery, swarm coordination, SLAM navigation) can be added as plugins
without modifying the core.

## Status

| Phase | Scope | Status |
| --- | --- | --- |
| Phase 0 | Architecture, ADRs, interfaces, SRS, engineering standards | ✅ Complete |
| Phase 1 | DroneOS Core (platform runtime) | 🟡 In progress — 1/6 packages |
| Phase 2 | Hardware Abstraction Layer (HAL) | 🟡 In progress — 0/8 packages |

### Phase 1 — DroneOS Core

| # | Package | Responsibility | Status |
| --- | --- | --- | --- |
| 1 | `drone_interfaces` | Shared ABCs, enums, DI contracts (no implementation) | ✅ Done |
| 2 | `drone_msgs` | Custom ROS messages/services/actions | ⬜ Not started |
| 3 | `drone_utils` | Central logger, config loader, utilities | ⬜ Not started |
| 4 | `drone_core` | Boot manager, state machine, health/mission/lifecycle/config managers, diagnostics publisher | ⬜ Not started |
| 5 | `drone_bringup` | Launch files, parameter loading, startup order | ⬜ Not started |
| 6 | `drone_dashboard` | Diagnostics/status backend (no GUI) | ⬜ Not started |

### Phase 2 — Hardware Abstraction Layer

| # | Package | Responsibility | Status |
| --- | --- | --- | --- |
| 1 | `drone_hal` | Hardware manager, registry, driver loader, discovery, lifecycle, diagnostics, DI | 🟡 In progress |
| 2 | `drone_camera` | Pi Camera Module driver (libcamera), frame acquisition, no processing | ⬜ Not started |
| 3 | `drone_fc` | Pixhawk/ArduPilot connection, heartbeat/mode/vehicle/battery/RC telemetry (no arm/takeoff/mission) | ⬜ Not started |
| 4 | `drone_rangefinder` | TFMini-S driver, distance measurement, filtering, calibration | ⬜ Not started |
| 5 | `drone_optical_flow` | Holybro PMW3901 driver, motion measurement, quality metrics | ⬜ Not started |
| 6 | `drone_gpio` | GPIO manager, LED/buzzer/general GPIO | ⬜ Not started |
| 7 | `drone_calibration` | Load/save/version calibration, sensor validation | ⬜ Not started |
| 8 | `drone_diagnostics` | CPU/RAM/temperature/sensor health aggregation | ⬜ Not started |

Each package is implemented, tested (`colcon test`), documented, and
committed individually — see that package's own `README.md` for what it
does and why, and its `docs/` folder for architecture, public API,
configuration, failure modes, and testing details.

## Repository layout

```
Drone_OS/
├── docs/                # Phase 0 architecture, ADRs, interfaces, SRS, standards
├── ros2_ws/
│   └── src/             # ROS 2 packages (one per row in the tables above)
├── configs/              # Reserved for deployment-level config overlays
├── scripts/               # Build / validation / deployment support (future)
├── tests/                 # Cross-package integration tests (future)
└── tools/                  # Developer tooling (future)
```

## Target hardware

- Companion computer: Raspberry Pi 4 Model B, Ubuntu Server 24.04 LTS, ROS 2 Jazzy
- Flight controller: Pixhawk 2.4.8 running ArduPilot
- Camera: Raspberry Pi Camera Module (libcamera)
- Rangefinder: TFMini-S (UART)
- Optical flow: Holybro PMW3901 (SPI)
- RC receiver: via Pixhawk

## Build

```bash
cd ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build
colcon test
colcon test-result --verbose
```

## License

Apache-2.0. See [LICENSE](LICENSE).
