# INC005 - Partner SFTP Transfer Failure
Incident: INC005
Severity: P2
Service: PartnerFileExchange

## Summary
Outbound partner files failed after the partner rebuilt its SFTP server.

## Root Cause
The partner host key changed. The integration correctly rejected the untrusted fingerprint.

## Resolution
The new fingerprint was independently verified through the approved partner-security process and then updated under change control.

## Lesson
Never bypass host-key validation merely to restore service.
