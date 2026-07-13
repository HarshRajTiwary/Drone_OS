# drone_msgs

Custom ROS 2 interface definitions for DroneOS Core. Definitions only —
no nodes, no logic. `ament_cmake` + `rosidl` (required for `.msg`/`.srv`/
`.action` generation; not a candidate for `ament_python`).

## Interfaces

| Type | Name | Wire form of |
| --- | --- | --- |
| msg | `SystemState` | `drone_interfaces.state_machine.SystemState` |
| msg | `HealthReport` | `drone_interfaces.health.HealthReport` |
| msg | `MissionInfo` | `drone_interfaces.mission.MissionMetadata` + `MissionState` |
| srv | `ActivateMission` | `IMissionRegistry.activate()` |
| srv | `DeactivateMission` | `IMissionRegistry.deactivate()` |
| srv | `ListMissions` | `IMissionRegistry.discover()` |
| action | `RunMission` | long-running mission execution (consumer: a later phase's Mission Execution Engine; defined now per Phase 1 scope) |

Numeric enum constants in these messages are independent of the Python
`drone_interfaces` enums' values (Python `Enum.auto()` starts at 1; ROS
msg constants here start at 0 by convention). `drone_utils` owns the
conversion tables between the two — see `docs/interfaces.md`.

## Dependencies

`builtin_interfaces`, `diagnostic_msgs` (reused for `KeyValue` rather than
redefining it).
