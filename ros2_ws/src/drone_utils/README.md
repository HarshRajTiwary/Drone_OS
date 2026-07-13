# drone_utils

Central logger, YAML configuration loader, and shared utilities for
DroneOS Core. `ament_python` (pure Python, no nodes of its own — see
`drone_core` for the boot-time node that wires these together).

## Modules

| Module | Implements |
| --- | --- |
| `logger.py` | `CentralLogger(ILogger)` — stdlib logging + optional rclpy node bridge |
| `config_loader.py` | `YamlConfigurationProvider(IConfigurationProvider)` — 5-domain YAML loader |
| `yaml_parser.py` | Safe YAML load/dump/dotted-key-get, used by the config loader and standalone |
| `time_utils.py` | Wall-clock/monotonic helpers, epoch <-> `builtin_interfaces/Time` conversion |
| `version_utils.py` | Installed-package version lookup, semver comparison |
| `error_helpers.py` | `error_boundary` context manager, `retry` decorator |
| `message_conversion.py` | `drone_interfaces` <-> `drone_msgs` wire-type conversion (the one place this mapping lives) |

## Dependencies

`drone_interfaces`, `drone_msgs`, `rclpy`, `builtin_interfaces`,
`ament_index_python`, `python3-yaml`.

## Testing

```bash
colcon test --packages-select drone_utils
```
