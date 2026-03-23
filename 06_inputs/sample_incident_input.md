# Sample Incident Input

## Incident name
Notification delivery failure

## Occurrence time
2026-03-20 14:35

## Impact scope
A portion of web users did not receive notification updates after message events.

## User impact
Users experienced delayed or missing notifications for core message actions.

## Recovery time
42 minutes

## Direct cause
Notification worker configuration was incorrect after release.

## Root cause
Release verification did not fully confirm notification delivery behavior in production-like conditions.

## Response timeline
- 14:35 incident detected
- 14:42 issue confirmed
- 14:55 rollback decision made
- 15:17 service recovered

## Exposed gaps
- Monitoring focused on API health, not business delivery success
- Release verification checklist missed notification delivery validation
- Ownership during release window was not explicit enough

## Existing corrective actions
- Rolled back configuration
- Added temporary manual verification step

## Expected output
Incident retrospective conclusion with systemic improvements and priorities.

Draft v1
