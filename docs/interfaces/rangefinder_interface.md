# Rangefinder Interface

## Purpose

This document defines the interface contract for the TFMini-S rangefinder used in DroneOS. It describes how the rangefinder is initialized, queried, monitored, and integrated into the platform.

## Scope

This document covers:

- Initialization and shutdown.
- Distance measurement acquisition.
- Diagnostics and error handling.
- Configuration and calibration expectations.

## Responsibilities

The rangefinder interface shall be responsible for:

- Establishing communication with the rangefinder.
- Providing distance measurements to the platform.
- Exposing measurement validity and timestamp information.
- Reporting health and device-level error conditions.

## Initialization

The interface shall support initialization procedures that validate device availability and readiness.

## Shutdown

The interface shall support a controlled shutdown that releases hardware resources and resets state.

## Measurement Acquisition

The interface shall provide a standard operation for retrieving a distance measurement with associated metadata, including:

- Measurement timestamp.
- Distance value.
- Validity or confidence information.
- Measurement sequence where available.

## Error Handling

The interface shall report:

- Communication failure.
- Invalid or out-of-range measurements.
- Timeout conditions.
- Device not available.

## Diagnostics

The interface shall expose diagnostics including:

- Readiness state.
- Recent measurement freshness.
- Error counts.
- Device health state.

## Configuration

Configuration should include:

- Connection settings.
- Measurement rate or polling interval.
- Range and scaling parameters.
- Calibration offsets where applicable.

## Assumptions

- The rangefinder is connected through a supported interface and accessible to the onboard software.
- The software consumer can treat measurements as normalized sensor observations.

## Limitations

- The interface does not define mission-specific use of the measurements.
- It does not prescribe hardware-specific low-level protocol details.

## Future Extensions

- Multi-rangefinder support.
- Higher-rate or fused ranging strategies.
- Additional quality metrics.
