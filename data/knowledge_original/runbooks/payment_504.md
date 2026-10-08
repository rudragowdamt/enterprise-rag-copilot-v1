---
title: Payment API HTTP 504 Troubleshooting
doc_type: runbook
system: PaymentAPI
environment: PROD
---
# Symptoms
Payment requests time out with HTTP 504, often after a release or downstream latency increase.
# Checks
1. Confirm API gateway and application latency for the affected window.
2. Check PaymentAPI deployment health and recent configuration changes.
3. Validate downstream LedgerService response time and connection health.
4. Check database connection-pool saturation and thread exhaustion.
5. If impact is widespread for more than 10 minutes, invoke the P1 escalation procedure.
# Recovery
Rollback the latest release if the timing correlates with deployment and health checks fail. Otherwise isolate the slow downstream dependency before increasing timeouts.
