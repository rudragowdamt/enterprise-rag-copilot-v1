# Generic API 5xx Troubleshooting Runbook
Document ID: RB-API-001

## Procedure
Capture correlation ID and timestamp; identify which layer produced the 5xx; trace client -> gateway -> integration runtime -> backend -> database/dependency; compare error rate and latency with baseline; check deployments and infrastructure events; inspect a representative transaction end-to-end; and search known-error and historical-incident records before changing production configuration.
