# INC004 - Integration Database Connectivity Degradation
Incident: INC004
Severity: P2
Service: CustomerSync

## Summary
Customer synchronization showed intermittent database connection-acquisition timeouts.

## Root Cause
A long-running reporting query consumed database resources and caused application connection pools to queue.

## Resolution
The database team terminated the problematic workload and tuned the query. Integration latency returned to baseline.
