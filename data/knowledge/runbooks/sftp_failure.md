# Enterprise SFTP Integration Failure
Document ID: RB-SFTP-001

## Symptoms
File transfer fails, authentication is rejected, host key changes, connection times out or files remain unprocessed.

## Checks
Confirm hostname/port, network reachability, service account status, SSH key validity, host-key fingerprint, remote directory permissions, filename convention, disk space and partner availability. A changed host key must be verified through an approved security channel before acceptance.

## Recovery
Retry a controlled file after the dependency is restored and confirm that duplicate-file protection prevents duplicate business processing.
