# Middleware Certificate Expiry Runbook
Document ID: RB-CERT-001

## Symptoms
TLS handshake failures, PKIX/trust errors, API authentication failures or sudden connectivity loss around a certificate expiry/rotation.

## Checks
Identify the certificate presented on the failing path, inspect expiry and chain, determine whether the issue concerns identity or trust, validate hostname/SAN, confirm intermediate certificates, and check relevant gateway/runtime truststores. Compare against recent certificate-change records.

## Prevention
Monitor certificates before expiry, maintain ownership metadata and test rotations in non-production before production implementation.
