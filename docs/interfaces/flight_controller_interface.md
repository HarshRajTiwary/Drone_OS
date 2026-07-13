# Flight Controller Interface

## Purpose

This document defines the interface contract between DroneOS and the Pixhawk 2.4.8 flight controller running ArduPilot firmware. The interface is intended to remain stable across mission logic and to abstract device-specific command and telemetry details.

## Scope

This document covers:

- Initialization and connection handling.
- Command transmission.
- Telemetry consumption.
- State reporting.
- Error handling and diagnostics.

## Responsibilities

The flight controller interface shall be responsible for:

- Establishing a connection to the flight controller.
- Sending high-level vehicle commands.
- Receiving telemetry and state updates.
- Reporting health and connection status.
- Translating platform-level instructions into MAVLink/MAVSDK-compatible operations where needed.

## Initialization

The interface shall support startup procedures that:

- Establish communication with the flight controller.
- Verify firmware and connection compatibility.
- Report readiness state.

## Shutdown

The interface shall support a safe shutdown or disconnect process that does not leave the vehicle in an ambiguous state.

## Command Interface

The interface shall support commands for:

- Mode changes.
- Takeoff and landing requests.
- Position, velocity, or attitude guidance where supported.
- Abort or fail-safe actions.

## Telemetry

The interface shall provide telemetry including:

- Vehicle state.
- Attitude and position information where available.
- Battery and status information.
- Connection and health indicators.

## Error Handling

The interface shall report:

- Communication loss.
- Timeout conditions.
- Invalid command response.
- Flight controller health degradation.

## Diagnostics

The flight controller interface shall expose diagnostics such as:

- Connection state.
- Last successful command time.
- Recent error counts.
- Telemetry freshness.

## Configuration

The interface shall support configuration for:

- Connection parameters.
- Command rate and timeout policy.
- Flight mode mapping.
- Telemetry update expectations.

## Assumptions

- ArduPilot and MAVLink/MAVSDK integration are available on the target system.
- The hardware path supports reliable and timely communication.

## Limitations

- The interface does not define the low-level firmware behavior of ArduPilot.
- It does not prescribe specific autopilot tuning values.

## Future Extensions

- Additional command modes for new missions.
- More advanced telemetry fusion and telemetry filtering.
- Integration with more autonomous control modes.
