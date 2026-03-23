# Sample Quality Gate Input

## Project name
AI Assistant Web

## Release name
v0.9.3

## Planned release time
2026-03-25 20:00

## Change scope
- Added new conversation entry
- Updated login flow
- Fixed message retry issue
- Refactored notification module

## Known risks
- Notification module changed in multiple files
- Login flow has limited regression coverage on edge cases

## Defect status
- P0: 0
- P1: 0
- P2: 2 open
- P3: 3 open

## Test coverage
- Core flow covered
- Partial regression on login edge cases
- Notification regression completed for main path only

## Regression result
- Main regression passed
- No blocker found
- Two medium-risk defects still open

## Monitoring readiness
- Core API monitoring ready
- Login error rate dashboard ready
- Notification success-rate monitoring not fully verified

## Rollback plan
- Application rollback available
- Database rollback not required for this release

## Current blockers
- No blocker issue
- Need confirmation for notification monitoring before release

## Expected output
Quality gate review conclusion with actions and priority.

Draft v1
