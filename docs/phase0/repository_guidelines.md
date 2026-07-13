# Repository Guidelines

## Purpose

This document defines the repository organization, contribution expectations, and change-management practices for DroneOS. It is intended to support a multi-engineer development environment with clear ownership and maintainable structure.

## Scope

This document covers:

- Repository structure.
- Module ownership expectations.
- Contribution standards.
- Review and approval expectations.
- Documentation and asset placement.

## Repository Structure

The repository should be organized into logical areas that reflect the architecture:

- src/ for core platform runtime and libraries.
- missions/ for mission plugins and mission-specific components.
- interfaces/ for interface definitions and shared contracts.
- configs/ for YAML configuration files.
- tests/ for unit, integration, simulation, and hardware tests.
- docs/ for architecture, requirements, and process documents.
- scripts/ for build, validation, and deployment support.

## Ownership Model

Each major subsystem should have a clear owner or maintainers group. Ownership should be documented in repository metadata or contributor documentation where applicable.

## Contribution Expectations

Contributors should:

- Follow the documented coding standards.
- Keep changes limited to the relevant subsystem where possible.
- Add or update tests for behavior changes.
- Update documentation when behavior, interfaces, or configuration change.
- Ensure reviews are completed before merging significant changes.

## Change Review Requirements

All non-trivial changes should be reviewed by at least one appropriate reviewer. Safety-critical, flight-control-related, or configuration-related changes should receive additional scrutiny.

## Branching and Merge Expectations

- Use feature branches for development work.
- Keep mainline branches stable and release-ready.
- Merge only after tests and review requirements are satisfied.
- Avoid merging speculative or incomplete changes into protected branches.

## Documentation Placement

- Architecture and requirements documents belong in docs/.
- Interface definitions should remain in the interfaces/ area or an equivalent documented location.
- Mission-specific documentation should be placed with the relevant mission plugin or architecture package.

## Configuration and Asset Management

- Keep configuration defaults in versioned YAML files.
- Do not embed secrets or credentials in repository files.
- Keep generated artifacts out of the source tree unless explicitly approved.

## Conclusion

The repository should remain structured, reviewable, and maintainable as the platform grows. Clear boundaries and ownership expectations reduce the risk of architectural drift and support long-term reliability.
