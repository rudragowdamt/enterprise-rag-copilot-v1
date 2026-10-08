---
title: Database Connection Pool Exhaustion
doc_type: runbook
system: OrderService
environment: PROD
---
# Symptoms
HTTP 503, increasing latency, and errors indicating no database connection is available.
# Checks
Review active versus maximum pool connections, long-running queries, database health, connection leaks and traffic spikes.
# Recovery
Do not simply raise pool limits. Remove the underlying leak or query bottleneck; use controlled restart only under the operational procedure.
