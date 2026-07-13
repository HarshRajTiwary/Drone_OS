# drone_utils — Configuration

`YamlConfigurationProvider(config_dir)` reads five files from
`config_dir`, each optional: `global_config.yaml`, `mission_config.yaml`,
`hardware_config.yaml`, `safety_config.yaml`, `logging_config.yaml`. A
missing file yields an empty domain; a malformed one raises
`ConfigurationError` (from `yaml_parser.load_yaml_file`).

`drone_bringup` (package 5) owns the actual `config_dir` deployed at
runtime and passes its path to `drone_core`'s Configuration Manager,
which constructs one `YamlConfigurationProvider` for the whole platform.
