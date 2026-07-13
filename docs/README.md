# DroneOS Documentation

## Purpose

This document establishes the Phase 0 documentation baseline for DroneOS, a modular autonomous drone operating system intended to support multiple missions without modifying the platform core. The documentation set is written for long-term maintenance by a multi-engineer organization and provides the architectural, process, and engineering foundation for subsequent implementation and integration work.

## Project Summary

DroneOS is an autonomous flight software platform for a Raspberry Pi 4 companion computer, a Pixhawk 2.4.8 flight controller running ArduPilot, and ROS 2 Jazzy on Ubuntu Server 24.04 LTS. The system is designed to support a mission-agnostic runtime that can host interchangeable mission plugins while preserving strict safety, reliability, observability, and configurability requirements.

The initial mission is:

- GPS-denied QR precision landing

Future missions will be enabled through a plugin architecture and shared platform services, including:

- AI target following
- Inspection
- Mapping
- Delivery
- Swarm coordination
- SLAM navigation

## Documentation Objectives

The documentation in this set is intended to:

- Define the architectural principles of DroneOS.
- Establish a production-grade software engineering baseline.
- Separate core platform responsibilities from mission-specific logic.
- Document interfaces, configuration, and operational processes.
- Support testability, debugging, review, and maintainability across the project lifecycle.

## Documentation Structure

The documentation is organized into the following areas:

### Architecture

- [architecture/high_level_architecture.md](architecture/high_level_architecture.md) — System-level architecture and core layers.
- [architecture/software_architecture.md](architecture/software_architecture.md) — Detailed runtime and component architecture.
- [architecture/system_context.md](architecture/system_context.md) — External actors, services, and environmental context.
- [architecture/module_diagrams.md](architecture/module_diagrams.md) — Module structure and dependencies.
- [architecture/sequence_diagrams.md](architecture/sequence_diagrams.md) — Runtime interaction flows.
- [architecture/deployment_architecture.md](architecture/deployment_architecture.md) — Deployment topology and host responsibilities.

### Phase 0 Engineering Baseline

- [phase0/software_requirements_specification.md](phase0/software_requirements_specification.md) — Formal requirements for the initial platform release.
- [phase0/project_scope.md](phase0/project_scope.md) — Scope, exclusions, constraints, and feasibility boundaries.
- [phase0/design_decisions.md](phase0/design_decisions.md) — Key design choices and rationale.
- [phase0/coding_standards.md](phase0/coding_standards.md) — Engineering conventions for Python, C++, ROS 2, and configuration.
- [phase0/repository_guidelines.md](phase0/repository_guidelines.md) — Repository structure, ownership, and contribution expectations.
- [phase0/development_workflow.md](phase0/development_workflow.md) — Build, test, review, and release workflow.
- [phase0/git_strategy.md](phase0/git_strategy.md) — Branching, merge, release, and rollback strategy.
- [phase0/testing_strategy.md](phase0/testing_strategy.md) — Unit, integration, hardware, simulation, and regression strategy.
- [phase0/configuration_strategy.md](phase0/configuration_strategy.md) — YAML-driven configuration hierarchy and runtime overrides.
- [phase0/logging_strategy.md](phase0/logging_strategy.md) — Centralized logging format, retention, and operational use.
- [phase0/error_handling_strategy.md](phase0/error_handling_strategy.md) — Fault handling, escalation, and recovery patterns.
- [phase0/documentation_standards.md](phase0/documentation_standards.md) — Documentation quality expectations and review standards.

### Interfaces

- [interfaces/camera_interface.md](interfaces/camera_interface.md)
- [interfaces/flight_controller_interface.md](interfaces/flight_controller_interface.md)
- [interfaces/rangefinder_interface.md](interfaces/rangefinder_interface.md)
- [interfaces/optical_flow_interface.md](interfaces/optical_flow_interface.md)
- [interfaces/mission_interface.md](interfaces/mission_interface.md)
- [interfaces/dashboard_interface.md](interfaces/dashboard_interface.md)

### Architecture Decision Records

- [decisions/adr_0001_project_structure.md](decisions/adr_0001_project_structure.md)
- [decisions/adr_0002_ros_architecture.md](decisions/adr_0002_ros_architecture.md)
- [decisions/adr_0003_hardware_abstraction.md](decisions/adr_0003_hardware_abstraction.md)
- [decisions/adr_0004_mission_plugin_system.md](decisions/adr_0004_mission_plugin_system.md)
- [decisions/adr_0005_logging.md](decisions/adr_0005_logging.md)

## Architectural Principles

DroneOS is defined by the following principles:

- Modularity: Platform services and mission logic must remain independently deployable.
- Reusability: Shared infrastructure must be reusable across multiple missions.
- Mission independence: Mission plugins must never modify core platform behavior.
- Hardware abstraction: Hardware devices must be represented through stable interfaces.
- Dependency injection: Components should be configured through typed interfaces and dependency injection.
- Configurability: Runtime behavior must be configurable using YAML.
- Observability: Every subsystem must expose diagnostics and health state.
- Safety-first design: Safety-critical behavior must be isolated, verified, and protected by explicit fail-safe paths.

## Document Conventions

All documents in this set should follow these conventions:

- Use clear, implementation-neutral technical language.
- Prefer explicit architectural rationale over speculative detail.
- Document assumptions, limitations, and future extensions.
- Use consistent terminology across all modules and interfaces.
- Express safety and reliability concerns as first-class design requirements.

## Phase 0 Status

This documentation package establishes the Phase 0 baseline for DroneOS. It is intended to support planning, architecture review, and implementation handoff. Subsequent work should extend this baseline into concrete modules, interfaces, tests, and deployment assets.

## Maintenance Guidance

These documents should be reviewed and updated whenever:

- A subsystem interface changes.
- A new mission plugin is introduced.
- A safety or reliability requirement is revised.
- A deployment topology changes.
- A critical architectural decision is made or revised.

## Next Step

The next document to generate is the architecture overview at [architecture/high_level_architecture.md](architecture/high_level_architecture.md).
