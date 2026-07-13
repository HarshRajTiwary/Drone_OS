# Project Scope

## Purpose

This document defines the scope of the Phase 0 DroneOS effort. It establishes what is included in the initial delivery, what is explicitly excluded, and the major constraints that shape the architecture and implementation plan.

## Scope

### In Scope

- Development of a modular autonomous drone operating system architecture.
- Support for a GPS-denied QR precision landing mission.
- Implementation of platform services for configuration, diagnostics, safety, logging, and mission lifecycle management.
- Definition of hardware abstractions for the selected onboard sensors and flight controller.
- Creation of Phase 0 documentation, interfaces, and engineering standards.
- Establishment of a testing and validation strategy appropriate for embedded robotics.

### Out of Scope

- Full commercial certification or regulatory approval.
- Full multi-vehicle swarm operations.
- Advanced AI-based perception beyond the initial mission scope.
- Full outdoor navigation beyond the planned mission constraints.
- Production packaging, field deployment operations, and manufacturing processes.

## Objectives

The Phase 0 effort aims to produce a stable architectural and engineering foundation for DroneOS. The deliverables should demonstrate that the system:

- Is modular and mission-independent at the platform level.
- Supports interchangeable mission plugins.
- Maintains safety-critical logic in a protected architecture.
- Can be tested, reviewed, and maintained by a multi-engineer team.

## Constraints

- Hardware platform is fixed to Raspberry Pi 4, Pixhawk 2.4.8, ArduPilot, Ubuntu Server 24.04 LTS, and ROS 2 Jazzy.
- Initial mission is GPS-denied QR precision landing.
- The system must remain understandable and maintainable over long-term development.
- The architecture must support future extensions without invasive core changes.

## Assumptions

- The chosen hardware components will remain available and compatible with the planned interfaces.
- Mission developers will work within the Mission SDK and platform contracts.
- Safety considerations will be treated as mandatory design requirements rather than optional enhancements.

## Risks and Considerations

- Perception performance may be affected by lighting or environmental variation.
- Sensor integration may reveal timing or reliability constraints that impact the mission design.
- Safety and testing requirements may increase the effort required for validation.

## Deliverables

- Architecture documentation.
- Interface definitions.
- Engineering standards and workflow documentation.
- Testing and configuration strategies.
- Initial requirements baseline for implementation.

## Future Scope

Subsequent phases can expand the system to include:

- AI target following.
- Inspection missions.
- Mapping.
- Delivery.
- Swarm operations.
- SLAM navigation.

## Conclusion

The Phase 0 scope is intentionally focused on establishing a robust architectural and engineering baseline for DroneOS. The project is not yet a full autonomous mission stack, but it is structured to become one without sacrificing maintainability or safety.
