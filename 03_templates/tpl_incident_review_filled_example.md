# Template Incident Review Filled Example

## Conclusion
The incident was caused by a release verification gap and insufficient business-level monitoring, not only by a configuration mistake.

## Key issues
- Notification delivery was not validated in production-like conditions
- Monitoring covered API health but not delivery success
- Release-window ownership was not explicit enough

## Analysis
The direct cause was an incorrect notification worker configuration after release. The deeper issue was that release verification did not confirm end-to-end notification delivery behavior under realistic conditions. In addition, monitoring focused on technical availability rather than business delivery success, which delayed precise detection. Ownership during the release window also lacked enough clarity.

## Recommended actions
1. Add notification delivery verification to the release checklist.
2. Add business-level success monitoring for notification delivery.
3. Define explicit release-window owner and watch responsibilities.
4. Convert this incident into a regression scenario for future releases.

## Priority
- High

## Director reminder
Do not treat this as a one-off config mistake. Fix the verification model and monitoring model together.

Draft v1
