# Wire form of drone_interfaces.state_machine.SystemState.
# Numeric values are independent of the Python enum's auto() ordering;
# drone_utils/drone_core own the conversion between the two.
uint8 BOOTING=0
uint8 INITIALIZING=1
uint8 READY=2
uint8 MISSION_RUNNING=3
uint8 PAUSED=4
uint8 ERROR=5
uint8 SHUTDOWN=6

uint8 state
string reason
builtin_interfaces/Time stamp
