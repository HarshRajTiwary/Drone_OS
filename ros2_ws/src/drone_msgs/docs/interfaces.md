# drone_msgs — Interfaces

## SystemState.msg

`uint8 state` (BOOTING=0, INITIALIZING=1, READY=2, MISSION_RUNNING=3,
PAUSED=4, ERROR=5, SHUTDOWN=6), `string reason`, `builtin_interfaces/Time stamp`.

## HealthReport.msg

`string component`, `uint8 status` (OK=0, DEGRADED=1, WARNING=2,
CRITICAL=3, UNKNOWN=4), `string message`, `builtin_interfaces/Time stamp`,
`diagnostic_msgs/KeyValue[] metrics`.

## MissionInfo.msg

`string name`, `string version`, `string description`, `uint8 state`
(UNINITIALIZED=0, INITIALIZED=1, RUNNING=2, PAUSED=3, COMPLETED=4,
ABORTED=5, FAILED=6).

## ActivateMission.srv / DeactivateMission.srv / ListMissions.srv

Request/response pairs matching `IMissionRegistry.activate(name,
config)`, `.deactivate(name)`, `.discover()` from `drone_interfaces`.
`config_yaml` carries mission-specific YAML as a string rather than a
structured field, matching the configuration strategy's YAML-only rule.

## RunMission.action

Goal: `mission_name`, `config_yaml`. Result: `success`, `message`.
Feedback: `progress_percent`, `status_message`. No implementation exists
yet in any phase; this is the wire contract a future Mission Execution
Engine will use.

## Conversion ownership

`drone_msgs` never imports `drone_interfaces` (a `rosidl` package cannot
depend on a Python ABC package) and `drone_interfaces` never imports
`drone_msgs` (it must stay usable without a ROS 2 runtime). The
conversion functions between the two live in `drone_utils`.
