# ADR-0003: Hardware Abstraction

## Context

DroneOS must support a variety of sensors and interfaces while remaining stable as hardware evolves. Direct coupling of platform logic to concrete devices would create brittle code and make testing and future upgrades difficult.

## Decision

All hardware devices, including the camera, rangefinder, optical flow sensor, and flight controller, shall be accessed through stable interfaces. Concrete device adapters will implement these interfaces, and core services will depend only on abstractions.

## Consequences

### Positive

- Easier testing with simulated components.
- Reduced maintenance overhead when hardware changes.
- More modular and reusable platform logic.

### Negative

- Additional interface and adapter design effort is required.
- Teams must respect the abstraction model during implementation.

## Alternatives Considered

- Direct integration of hardware drivers into core platform modules.
- Maintaining separate code paths for every device variant.

## Conclusion

Hardware abstraction is essential to making DroneOS modular, testable, and maintainable.
