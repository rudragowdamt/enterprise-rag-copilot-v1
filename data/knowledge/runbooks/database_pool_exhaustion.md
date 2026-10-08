# Integration Database Connection Pool Exhaustion
Document ID: RB-DB-001

## Symptoms
Connection acquisition timeout, increased integration latency, 5xx errors and queued transactions.

## Checks
Measure active/idle/max connections, database availability, long-running queries, leaked connections and traffic spikes. Determine whether pool exhaustion is the cause or a symptom of database slowness. Do not increase pool limits without validating database capacity.

## Recovery
Resolve the underlying database/query issue, allow connections to recover, then validate integration latency and error rate.
