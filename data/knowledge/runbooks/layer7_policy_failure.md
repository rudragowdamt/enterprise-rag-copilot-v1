# Layer7 Gateway Policy Failure Runbook
Document ID: RB-L7-002
Platform: Broadcom Layer7 API Gateway

## Symptoms
API returns unexpected 4xx/5xx responses after a policy deployment or migration.

## Procedure
Identify the policy revision, compare it with the last known-good version, inspect failed assertions, validate context variables and routing assertions, check referenced encapsulated assertions, certificates and cluster properties, and correlate gateway audit logs with the request ID. If the incident began immediately after an approved deployment, follow rollback criteria rather than making untracked production edits.
