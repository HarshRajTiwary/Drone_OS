# Git Strategy

## Purpose

This document defines the Git strategy for DroneOS. It is intended to support a controlled, collaborative, and maintainable development process for a multi-engineer robotics software project.

## Scope

This document covers:

- Branching strategy.
- Merge policy.
- Release management.
- Commit expectations.
- Rollback and recovery considerations.

## Branching Strategy

### Main Branches

- main: The stable branch for tested and release-ready changes.
- develop: The integration branch for ongoing work, if used by the team.

### Supporting Branches

- feature/*: For new functionality.
- fix/*: For bug fixes.
- hotfix/*: For urgent production or release issues.
- release/*: For release preparation.

## Merge Policy

- All changes to main should be made through reviewed pull requests or merge requests.
- Feature branches should be kept short-lived and rebased or merged regularly to avoid drift.
- Large changes should be broken into smaller, reviewable units where possible.

## Commit Guidelines

- Commit messages should be descriptive and specific.
- Avoid mixing unrelated changes in a single commit.
- Include context in commit messages when the change affects safety, interfaces, or configuration.

## Release Management

- Releases should be tagged clearly and documented.
- Release branches should be used when release-specific stabilization is required.
- Each release should include a summary of changes, known issues, and validation evidence.

## Rollback Strategy

When a change introduces a defect or safety concern:

- Revert the change through a reviewed commit or merge.
- Preserve the evidence of the problem and the fix.
- Update tests or documentation to avoid recurrence.

## Conclusion

The Git strategy should support disciplined collaboration and safe change management. It must preserve the integrity of the mainline branch while enabling fast iteration on new features and fixes.
