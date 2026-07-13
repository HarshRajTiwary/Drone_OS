# Development Workflow

## Purpose

This document defines the development workflow for DroneOS. It describes how work should be planned, implemented, reviewed, validated, and released in a way that supports safety, quality, and maintainability.

## Scope

This document covers:

- Planning and task definition.
- Implementation expectations.
- Review and validation workflow.
- Release readiness criteria.

## Development Lifecycle

### 1. Planning

Work should begin with clear requirements, architecture guidance, and documented acceptance criteria. The planning stage must identify the subsystem affected, the expected interfaces, and the testing strategy.

### 2. Implementation

Implementation should proceed incrementally with small, reviewable changes. Developers should work against defined interfaces and preserve platform safety expectations.

### 3. Review

Every non-trivial change should be reviewed by at least one appropriate reviewer. Review should focus on architecture, correctness, test coverage, documentation, and safety impact.

### 4. Validation

Validation must include relevant unit, integration, simulation, and hardware tests where applicable. Safety-sensitive changes require stronger validation and review.

### 5. Release

Releases should only proceed when the relevant tests have passed, the documentation is current, and the change has gone through the required review process.

## Workflow Expectations

- Use issue tracking or equivalent task management for planned work.
- Keep work items scoped and reviewable.
- Document assumptions and open questions during implementation.
- Avoid merging changes that are incomplete or lack appropriate validation.

## Review Checklist

A change should be considered review-ready when:

- The requirement is clear.
- The implementation matches the intended interface.
- Tests are included or updated.
- Documentation is updated where necessary.
- Safety and observability concerns are addressed.

## Release Readiness Criteria

A release is ready when:

- All required tests have passed.
- Important configuration and interface changes are documented.
- Known limitations are recorded.
- The release note or change summary is complete.

## Conclusion

A disciplined workflow is essential for a robotics platform that must remain safe and maintainable over time. The process should emphasize clarity, verification, and review.
