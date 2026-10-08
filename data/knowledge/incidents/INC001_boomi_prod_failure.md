# INC001 - Boomi Order Integration Failure
Incident: INC001
Severity: P1
Platform: Boomi
Service: OrderIntegration

## Summary
Production order messages stopped reaching ERP after a connection component was changed during a release.

## Findings
Boomi runtime was healthy. Process Reporting showed authentication failures against the ERP endpoint. The deployment contained an incorrect production credential reference.

## Resolution
The team rolled back the connection component to the last known-good packaged component, validated one order transaction, and then released queued processing.

## Lesson
Runtime health alone does not prove end-to-end integration health. Deployment and connection-component versions must be correlated during triage.
