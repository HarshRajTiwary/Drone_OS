# ADR-0005: Centralized Logging

## Context

DroneOS will include many subsystems, sensors, and mission behaviors. Without a centralized and structured logging approach, debugging, validation, and operations become significantly more difficult and error-prone.

## Decision

DroneOS shall use a centralized logging architecture in which all major subsystems publish structured logs to a shared logging service. Logs will be classified by severity, timestamped, and correlated with runtime context so they can support debugging, diagnostics, and post-mission analysis.

## Consequences

### Positive

- Stronger observability.
- Better incident analysis and debugging.
- Improved support for safety review and post-flight analysis.

### Negative

- Logging infrastructure and standards require discipline.
- Excessive logging can create storage and performance overhead.

## Alternatives Considered

- Independent subsystem logs with no shared coordination.
- Ad hoc print-based logging.

## Conclusion

Centralized structured logging is essential to the long-term reliability and maintainability of DroneOS.
