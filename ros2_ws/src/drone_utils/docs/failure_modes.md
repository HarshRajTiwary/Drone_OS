# drone_utils — Failure Modes

| Condition | Raised as | Where |
| --- | --- | --- |
| YAML file present but malformed | `ConfigurationError` | `yaml_parser.load_yaml_file`, propagates through `YamlConfigurationProvider.reload()`/`__init__` |
| YAML top level is not a mapping | `ConfigurationError` | `yaml_parser.load_yaml_file` |
| Malformed `major.minor.patch` string | `ValidationError` | `version_utils.parse_semver` |
| Unknown ROS 2 package queried for version | none — returns `'unknown'`, not an error | `version_utils.get_package_version` (a missing package is a normal, expected case at boot before every package is installed, not a fault) |
| Non-`DroneOSError` exception inside `error_boundary` | wrapped in the caller-specified `DroneOSError` subclass, original chained via `__cause__` | `error_helpers.error_boundary` |
| `retry()` exhausts all attempts | original exception re-raised unwrapped | `error_helpers.retry` |
