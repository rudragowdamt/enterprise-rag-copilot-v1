# INC002 - Layer7 Authentication Outage After Certificate Rotation
Incident: INC002
Severity: P1
Platform: Layer7
Service: CustomerAPI

## Summary
CustomerAPI returned HTTP 401 shortly after the identity provider rotated its signing certificate.

## Root Cause
Layer7 token validation was using stale signing-key/trust information.

## Resolution
The approved signing-key/trust configuration was refreshed and authentication tests passed.

## Lesson
For sudden widespread 401 responses, compare IdP key/certificate changes before assuming client credentials are incorrect.
