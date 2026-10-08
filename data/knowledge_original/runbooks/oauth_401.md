---
title: OAuth 401 Authentication Troubleshooting
doc_type: runbook
system: IdentityService
environment: PROD
---
# Symptoms
Applications receive HTTP 401 while requesting or using OAuth access tokens.
# Checks
Validate client ID and secret reference, token audience and scope, system clock skew, certificate validity, and the IdentityService token endpoint. Never copy secrets into tickets or the AI assistant.
# Recovery
Rotate an expired certificate or credential through the approved secret-management process, then retest token acquisition and one business transaction.
