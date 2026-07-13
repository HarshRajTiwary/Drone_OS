# Wire form of drone_interfaces.health.HealthReport.
uint8 OK=0
uint8 DEGRADED=1
uint8 WARNING=2
uint8 CRITICAL=3
uint8 UNKNOWN=4

string component
uint8 status
string message
builtin_interfaces/Time stamp
diagnostic_msgs/KeyValue[] metrics
