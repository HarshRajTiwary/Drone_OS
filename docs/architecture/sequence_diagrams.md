# Sequence Diagrams

## Purpose

This document describes the main runtime interaction flows within DroneOS. It captures how subsystems exchange control, commands, telemetry, and status information during startup, mission execution, and failure handling.

## Scope

This document covers:

- Boot sequence interactions.
- Mission execution flow.
- Hardware interaction flow.
- Safety intervention flow.
- Dashboard and telemetry reporting flow.

## Design Rationale

Sequence diagrams are essential for ensuring that complex robotics behaviors are understood across teams. They clarify the ordering of actions, dependencies between components, and how failure conditions are surfaced to the operator and recovery logic.

## Boot Sequence

The boot sequence describes how the system is brought from power-on into a mission-ready state.

```mermaid
sequenceDiagram
    participant O as Operator
    participant R as Runtime Orchestrator
    participant C as Configuration Service
    participant S as State Manager
    participant H as Hardware Abstraction
    participant F as Flight Controller
    participant D as Dashboard

    O->>R: Power on / start system
    R->>C: Load configuration
    C-->>R: Configuration validated
    R->>S: Initialize state
    R->>H: Initialize sensors
    H->>F: Connect and initialize
    F-->>H: Telemetry available
    H-->>D: Health and diagnostics
    R-->>D: System ready
```

## Mission Flow

The mission flow shows how a mission plugin interacts with platform services during the execution of the QR precision landing mission.

```mermaid
sequenceDiagram
    participant O as Operator
    participant M as Mission Manager
    participant P as Mission Plugin
    participant V as Vision Core
    participant N as Navigation
    participant S as Safety
    participant F as Flight Core
    participant FC as Flight Controller

    O->>M: Start mission
    M->>P: Initialize mission plugin
    P->>V: Request visual observations
    V-->>P: QR detection / pose estimate
    P->>N: Request landing trajectory
    N->>S: Validate trajectory
    S-->>N: Approved / rejected
    N-->>F: Motion command
    F->>FC: Send controlled command
    FC-->>F: Flight telemetry
    F-->>M: Mission progress update
    M-->>O: Mission status
```

## Hardware Interaction

This sequence shows how hardware devices are abstracted and used within the runtime.

```mermaid
sequenceDiagram
    participant H as Hardware Abstraction
    participant C as Camera
    participant R as Rangefinder
    participant O as Optical Flow
    participant V as Vision / Navigation

    H->>C: Initialize camera
    C-->>H: Frame stream
    H->>R: Initialize rangefinder
    R-->>H: Distance measurements
    H->>O: Initialize optical flow
    O-->>H: Motion estimates
    H-->>V: Normalized sensor data
```

## Safety Intervention

The safety intervention sequence shows how unsafe behavior is contained and surfaced.

```mermaid
sequenceDiagram
    participant M as Mission Logic
    participant S as Safety Supervisor
    participant F as Flight Core
    participant FC as Flight Controller
    participant D as Dashboard

    M->>F: Send command
    F->>S: Evaluate command
    S-->>F: Command approved or rejected
    alt Unsafe command
        S->>F: Override / abort
        F->>FC: Execute fail-safe behavior
        FC-->>D: Emergency state
    end
```

## Diagnostics and Telemetry Reporting

This sequence describes how health data is propagated through the system.

```mermaid
sequenceDiagram
    participant H as Subsystem
    participant D as Diagnostics Service
    participant L as Logger
    participant DB as Dashboard / Telemetry Sink

    H->>D: Publish health update
    D->>L: Write structured log
    D->>DB: Publish telemetry event
```

## Assumptions

- ROS 2 topic and service flows are available during runtime.
- The flight controller and companion computer remain connected.
- Safety checks are executed before critical commands are forwarded.

## Limitations

- These diagrams reflect the intended runtime flow and not every implementation-specific exception path.
- Detailed timing behavior is not prescribed in this document.

## Future Extensions

- Multi-vehicle coordination sequence diagrams.
- Recovery and replan sequences for mission failure.
- Remote operator handoff sequences.

## Conclusion

The sequence diagrams establish the expected interaction patterns across the DroneOS platform. They clarify how the system behaves during startup, mission execution, hardware access, safety intervention, and diagnostics reporting.
