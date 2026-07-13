# Wire form of drone_interfaces.mission.MissionMetadata + MissionState.
uint8 UNINITIALIZED=0
uint8 INITIALIZED=1
uint8 RUNNING=2
uint8 PAUSED=3
uint8 COMPLETED=4
uint8 ABORTED=5
uint8 FAILED=6

string name
string version
string description
uint8 state
