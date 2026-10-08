# INC003 - Payment API HTTP 504
Incident: INC003
Severity: P1
Platform: Axway
Service: PaymentService

## Summary
Payment API calls through Axway returned intermittent 504 responses.

## Investigation
Gateway nodes were healthy. Network connectivity succeeded, but backend response time increased beyond the gateway timeout. The payment backend was waiting on an exhausted database connection pool.

## Root Cause
Database slowness caused backend requests to exceed the API gateway timeout.

## Resolution
Database blocking activity was resolved and the application connection pool recovered. Gateway timeout was not increased.

## Lesson
A gateway 504 can be a downstream symptom. Trace the complete dependency chain before modifying gateway timeouts.
