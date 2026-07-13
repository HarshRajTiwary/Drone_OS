# Coding Standards

## Purpose

This document defines the coding, review, and engineering standards for DroneOS. It is intended to ensure that code developed for DroneOS remains consistent, maintainable, testable, and safe across teams and releases.

## Scope

This document covers standards for:

- Python development.
- C++ development.
- ROS 2 integration.
- Git usage.
- Logging and exception handling.
- Folder structure and dependency injection practices.
- Testing and formatting expectations.

## General Principles

DroneOS development shall follow these principles:

- Clarity over cleverness.
- Explicit interfaces over implicit behavior.
- Dependency injection over global state.
- Safety and observability over convenience.
- Readability and maintainability over micro-optimizations.

## Python Standards

### Style

- Follow PEP 8 and use a consistent style across the codebase.
- Prefer descriptive names and avoid ambiguous abbreviations.
- Keep functions focused and reasonably small.
- Use type hints for public APIs and significant internal interfaces.

### Structure

- Organize modules by responsibility.
- Keep platform logic separate from mission-specific logic.
- Avoid circular imports.
- Use clear package boundaries for hardware, navigation, safety, and missions.

### Conventions

- Use exceptions for exceptional conditions, not for regular control flow.
- Prefer immutable configuration objects or typed data structures for shared state.
- Avoid hidden side effects in constructors or module-level initialization.

## C++ Standards

### Style

- Follow a consistent C++ style guide and keep naming and formatting predictable.
- Prefer strong typing and explicit ownership semantics.
- Use RAII and avoid manual resource management where possible.
- Keep interfaces minimal and well documented.

### Structure

- Prefer small, focused classes and clear separation of responsibilities.
- Encapsulate hardware-specific behavior in adapters or interfaces.
- Avoid global mutable state.

## ROS 2 Standards

- Use topic names that are stable, descriptive, and version-aware.
- Keep message definitions narrow and semantically clear.
- Use services for synchronous interactions and actions for long-running tasks.
- Avoid direct coupling between mission plugins and concrete node implementations.

## Git Standards

- Use short-lived feature branches.
- Require pull requests for all merges to protected branches.
- Use descriptive commit messages and avoid mixing unrelated changes.
- Keep changes focused and reviewable.

## Naming Conventions

- Use descriptive, domain-specific names rather than vague placeholders.
- Prefer snake_case for Python and lower_snake_case for ROS 2 artifacts where applicable.
- Prefer PascalCase for C++ classes and camelCase only where a framework or existing convention requires it.
- Use consistent terminology across hardware, software, and mission modules.

## Logging Standards

- Use structured logging rather than ad hoc print statements.
- Log at appropriate severity levels and include context.
- Avoid logging sensitive data such as secrets or private operator information.
- Ensure that logging remains consistent across components.

## Exception Handling

- Catch specific exceptions rather than broad exceptions unless there is a compelling reason.
- Preserve diagnostic context when an exception is handled or re-raised.
- Use fail-safe and recovery strategies for safety-critical paths.
- Never silently swallow errors that affect safety, reliability, or observability.

## Folder Structure

The repository should follow a clear structure that separates:

- Core platform runtime.
- Hardware interfaces.
- Mission logic.
- Tests.
- Configuration.
- Documentation.

## Testing Standards

- Write tests for all critical logic paths.
- Unit tests must cover platform behavior independently of hardware.
- Integration tests must verify component interactions.
- Hardware and simulation tests must validate real-world conditions.

## Formatting

- Use automatic formatting tools where available.
- Ensure consistent indentation, line length, and import ordering.
- Keep comments focused on rationale and non-obvious behavior.

## Dependency Injection

- Components should receive dependencies through constructors or explicit configuration objects.
- Avoid hidden singletons where a dependency can be injected.
- Favor interfaces and explicit wiring for testability and reuse.

## SOLID Principles

Development should explicitly support:

- Single responsibility.
- Open/closed design.
- Liskov substitution where interfaces are used.
- Interface segregation.
- Dependency inversion.

## Conclusion

These standards are intended to keep DroneOS robust, understandable, and maintainable as the platform evolves from Phase 0 into future missions and releases.
