# Boomi Atom or Molecule Unavailable Runbook
Document ID: RB-BOOMI-002
Platform: Boomi

## Symptoms
Scheduled processes do not start, executions remain queued, or the runtime appears offline.

## Checks
1. Confirm runtime status in Boomi platform.
2. For Molecule deployments, determine whether one node or the complete cluster is affected.
3. Check host availability, CPU, memory, disk space and filesystem access.
4. Review runtime/container logs around the failure timestamp.
5. Validate outbound connectivity required by the runtime.
6. Confirm certificates and proxy configuration have not changed.
7. Restart a runtime only under the approved operational procedure.
8. For a multi-node Molecule, prefer controlled failover over restarting all nodes simultaneously.

## Recovery
After recovery, execute a health-check process and validate one end-to-end business transaction before releasing queued traffic.
