# Boomi SFTP Connector — Connection and Authentication Troubleshooting

## Document Metadata
Vendor: Boomi
Product: Boomi Integration — SFTP Connector
Category: SFTP Connectivity and Authentication
Document Type: Technical Troubleshooting Runbook
Source: https://help.boomi.com/docs/Atomsphere/Integration/Connectors/SFTP_connection
Source Status: Official vendor reference plus original diagnostic guidance
Error Codes: No universal error code assigned
Applicability: Current SFTP connector; verify against deployed connector version

## Problem
A Boomi integration fails when connecting to an SFTP server,
authenticating, or transferring files.

## Common Symptoms
- Connection timed out
- Connection refused
- Authentication failed
- SSH host key verification failure
- Permission denied when reading or writing files

These are general failure categories, not guaranteed exact Boomi error messages.

## Prerequisites
- Authorized access to Boomi execution details
- SFTP hostname and port
- SFTP account username
- Access to the relevant runtime or assistance from its administrator
- Approval before changing production configuration

Never include passwords, private keys, or secrets in incident tickets.

## Step 1 — Identify the Failed Execution
1. Open the relevant Boomi process execution details.
2. Locate the failed SFTP connector operation.
3. Record the process name, execution ID, timestamp and runtime.
4. Capture the sanitized error message.
5. Determine whether the failure occurred during connection,
   authentication, file listing, upload or download.

Expected Result:
The exact failure stage and affected SFTP connection are identified.

## Step 2 — Verify the SFTP Connection Configuration
Inspect the SFTP connection component.

Verify:
- Host: Correct SFTP hostname or IP address
- Port: Correct SSH/SFTP port (commonly 22)
- User Name: Correct authorized account
- Key Authentication: None, Key File Path or Key File Content
- Remote Directory: Correct target folder
- Connection Timeout (ms): Appropriate for the environment
- Read Timeout (ms): Appropriate for individual network reads

Expected Result:
Connection settings match the SFTP server configuration.

Do not change production values without authorization.

## Step 3 — Test TCP Connectivity (Windows Runtime)
Run from the Boomi runtime host or its equivalent network environment:

Test-NetConnection sftp.example.com -Port 22

Replace sftp.example.com and 22 with the actual endpoint details.

Expected Result:
TcpTestSucceeded : True

If False:
- Check hostname and DNS resolution.
- Check server availability.
- Check firewall rules and network routing.
- Confirm the server is listening on the configured port.

A successful TCP test does not prove SFTP authentication works.

## Step 4 — Test TCP Connectivity (Linux Runtime)
Run:

nc -vz -w 10 sftp.example.com 22

Expected Result:
A successful TCP connection message.

If nc is unavailable, request an approved equivalent from
the infrastructure team.

Do not assume a network test from your laptop represents
connectivity from the Boomi runtime.

## Step 5 — Verify SFTP Authentication
Confirm which authentication method the SFTP server expects.

For username/password:
- Verify the username.
- Confirm credentials are valid through an approved process.
- Check whether the account is locked or expired.

For SSH key authentication:
- Confirm the correct Key Authentication option.
- Verify the configured key file exists on the runtime if using a path.
- Confirm the runtime account has permission to read the key.
- Verify the matching public key is authorized on the SFTP server.
- Check the private key passphrase configuration if applicable.

Expected Result:
The SFTP server accepts the configured authentication method.

Avoid repeated login attempts that could lock the account.

## Step 6 — Verify SSH Host Key
Review the Known Host Entry configuration.

- Obtain the approved SFTP server host key or fingerprint
  through a trusted administrator or vendor channel.
- Compare it with the configured server identity.
- If the server host key has changed, investigate why.
- Update the trusted host entry only after verification.

Expected Result:
The configured server identity matches the trusted server.

Never disable host key verification simply to bypass a mismatch.

## Step 7 — Test SFTP Login (Authorized Linux/Windows Client)
Where an approved SSH client is available, run:

sftp -P 22 sftpuser@192.0.2.10

Verify the server host key against an independently trusted
fingerprint before accepting a first-time connection.

For an approved private key:

sftp -i /path/to/private_key -P 22 sftpuser@192.0.2.10

Expected Result:
An interactive sftp> prompt after successful authentication.

For a non-production test account, permitted diagnostic
commands may include:

pwd
ls

Do not upload, delete, rename, or modify production files
during diagnostic testing without authorization.

## Step 8 — Verify Remote Directory Permissions
Check:
- Remote Directory path
- Directory existence
- Read permission for download/list operations
- Write permission for upload operations
- Server-side folder restrictions

Expected Result:
The account can access the intended directory and perform
the authorized file operation.

## Step 9 — Review Timeout Settings
Check Connection Timeout (ms) and Read Timeout (ms).

Connection Timeout concerns establishing the connection.
Read Timeout concerns individual network read operations,
not necessarily the entire file transfer duration.

Check server-side timeout settings and network latency.

Change values only with approval and supporting evidence.

## Step 10 — Validate the Resolution
1. Execute an approved non-production or controlled test.
2. Confirm SFTP authentication succeeds.
3. Confirm the expected file operation completes.
4. Review Boomi execution details for errors.
5. Verify downstream processing and file integrity.
6. Check for duplicate or partially processed files.

Expected Result:
The process completes successfully without unexpected
business side effects.

## Escalation Evidence
- Process and execution identifiers
- Failure timestamp and timezone
- Runtime environment
- SFTP connector version
- Sanitized error message
- Target hostname and port
- TCP connectivity result
- Authentication method (not credentials)
- Host key verification outcome
- Relevant server-side logs

## Source References
Boomi SFTP connection:
https://help.boomi.com/docs/Atomsphere/Integration/Connectors/SFTP_connection

Boomi SFTP connector:
https://help.boomi.com/docs/Atomsphere/Integration/Connectors/SFTP_connector

## RAG Answering Rules
- Provide numbered technical steps with expected results.
- Distinguish verified vendor configuration from general diagnostics.
- Do not invent vendor error codes or product-specific commands.
- Do not expose credentials, private keys, or sensitive file contents.
- Request missing environment details when exact instructions depend on them.
- Cite the source document used.

