# drone_interfaces — Configuration

`drone_interfaces` has no YAML configuration of its own. It contains no
nodes, no parameters, and no runtime state to configure.

It defines `ConfigDomain` (`drone_interfaces.configuration`), the enum
that `drone_utils`'s Configuration Loader uses to organize the platform's
actual YAML files, per `docs/phase0/configuration_strategy.md`:

| `ConfigDomain` member | Corresponding YAML file (owned by `drone_utils` / `drone_bringup`, package 3 & 5) |
| --- | --- |
| `GLOBAL` | `global_config.yaml` |
| `MISSION` | `mission_config.yaml` |
| `HARDWARE` | `hardware_config.yaml` |
| `SAFETY` | `safety_config.yaml` |
| `LOGGING` | `logging_config.yaml` |

This package only fixes the *names* of these domains so that every
consumer of `IConfigurationProvider` refers to the same five domains by
the same identifiers. The files themselves, their schemas, and their
validation rules are implemented in `drone_utils`.
