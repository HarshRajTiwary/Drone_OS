# drone_msgs — Testing

Definitions-only package: correctness is generation succeeding and
`ament_lint_auto`/`ament_lint_common` passing (package.xml/CMakeLists
formatting, msg/srv/action lint). No pytest suite is added here —
message field/constant correctness is exercised where these types are
actually used, in `drone_utils`'s conversion-function tests and
`drone_core`'s node tests.

```bash
colcon build --packages-select drone_msgs
colcon test --packages-select drone_msgs
```
