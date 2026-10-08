# Layer7 OAuth HTTP 401 Troubleshooting
Document ID: RB-L7-001
Platform: Broadcom Layer7 API Gateway

## Symptoms
Clients receive HTTP 401 while the backend service may remain healthy.

## Checks
1. Determine whether rejection occurs at the gateway or backend.
2. Validate Authorization header presence and token format.
3. Check token expiration, issuer, audience and required scopes.
4. Validate OAuth/JWT verification policy and identity-provider availability.
5. Check signing certificate/JWK rotation and gateway trust configuration.
6. Review recent policy migrations or configuration changes.
7. Confirm clock synchronization when token time claims appear invalid.
8. Use a known-good token for a controlled test; never place production secrets in incident notes.

## Common Causes
Expired token, incorrect audience/scope, rotated signing key, stale JWK cache, IdP outage, or an incorrect gateway policy.
