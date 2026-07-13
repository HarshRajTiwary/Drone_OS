# ADR-0002: ROS 2 Architecture

## Context

The platform requires a middleware backbone that can support modular components, asynchronous telemetry, service-based interactions, and future mission extensibility. The architecture must support real-time and event-driven behavior while remaining maintainable.

## Decision

ROS 2 Jazzy shall be used as the primary middleware framework for DroneOS. Components shall communicate using topics for streaming data, services for synchronous requests, and actions for long-running mission behavior. The architecture will treat ROS 2 as the integration backbone rather than a hidden implementation detail.

## Consequences

### Positive

- Strong support for modular component interaction.
- Clear separation between producers and consumers of data.
- Good compatibility with modern robotics tooling and ecosystem practices.

### Negative

- Teams must understand ROS 2 lifecycle and communication semantics.
- Middleware abstractions can add some runtime complexity.

## Alternatives Considered

- A custom in-process message bus.
- A non-ROS framework or proprietary middleware.

## Conclusion

ROS 2 Jazzy provides the required architectural flexibility and ecosystem support for DroneOS.
