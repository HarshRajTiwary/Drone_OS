# Camera Interface

## Purpose

This document defines the interface contract for the camera subsystem in DroneOS. It describes the responsibilities, operations, lifecycle, diagnostics, and configuration expectations for camera access and image acquisition.

## Scope

This document covers the platform-level interface for:

- Camera initialization.
- Image capture.
- Frame metadata exposure.
- Calibration management.
- Error handling and diagnostics.

## Responsibilities

The camera interface shall be responsible for:

- Establishing a hardware connection to the camera.
- Providing image frames to the perception stack.
- Exposing frame metadata such as timestamps and camera parameters.
- Supporting calibration and configuration retrieval.
- Reporting device health and error conditions.

## Initialization

The camera subsystem shall support initialization operations that:

- Confirm device availability.
- Configure the camera for the selected runtime mode.
- Validate the connection and readiness state.

## Shutdown

The interface shall support a controlled shutdown path that releases camera resources and resets state cleanly.

## Capture

The interface shall provide a standard operation for acquiring image frames. The operation should return a frame object or equivalent abstraction containing:

- The image payload.
- Timestamp.
- Frame sequence identifier where available.
- Quality or validity information.

## Frame Metadata

The camera interface shall expose frame metadata including:

- Capture timestamp.
- Image dimensions.
- Frame identifier.
- Exposure or acquisition parameters where relevant.
- Calibration state.

## Calibration

The interface shall support:

- Retrieval of calibration parameters.
- Validation of calibration state.
- Explicit indication when calibration is missing or invalid.

## Error Handling

The camera interface shall report:

- Device not available.
- Capture failure.
- Configuration error.
- Timeout or degraded acquisition state.

## Diagnostics

The camera subsystem shall expose diagnostics describing:

- Readiness.
- Connection state.
- Last successful capture time.
- Error count or recent error conditions.

## Configuration

The camera configuration shall include:

- Resolution.
- Frame rate.
- Exposure or gain parameters where applicable.
- Calibration source and identifiers.

## Assumptions

- The camera hardware is accessible through the companion computer environment.
- The image pipeline expects a normalized frame representation.

## Limitations

- This interface does not prescribe low-level driver implementation details.
- It does not define mission-specific image processing behavior.

## Future Extensions

- Multi-camera support.
- Advanced timing or synchronization features.
- Embedded preprocessing or compression support.
