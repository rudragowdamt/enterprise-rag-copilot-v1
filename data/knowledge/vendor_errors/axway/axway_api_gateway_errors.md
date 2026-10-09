# Axway API Gateway — Authentication, Authorization and Rate-Limiting Troubleshooting

## Scenario 1: HTTP 401 Unauthorized

Platform: Axway API Gateway
Category: Authentication
Symptoms: An API request returns HTTP 401.

Possible causes:
- Missing or invalid authentication credentials.
- Expired or invalid access token.
- Incorrect token issuer, audience, or signature validation configuration.
- Authentication policy failure.

Troubleshooting:
1. Check API Gateway transaction logs and policy execution details.
2. Verify the configured authentication mechanism.
3. Validate token expiry, issuer, audience, and signature where applicable.
4. Confirm credentials are being sent correctly.
5. Compare the request with a known successful request.

Resolution:
- Supply valid credentials or refresh the token.
- Correct authentication policy configuration where appropriate.
- Avoid logging sensitive tokens or passwords.

## Scenario 2: HTTP 403 Forbidden

Platform: Axway API Gateway
Category: Authorization
Symptoms: An authenticated client receives HTTP 403.

Possible causes:
- Insufficient API permissions.
- Missing required scopes or roles.
- Access-control policy denies the request.
- Client application is not authorized for the API.

Troubleshooting:
1. Verify whether authentication succeeded.
2. Review authorization policy execution and gateway logs.
3. Check the client's assigned scopes, roles, and API permissions.
4. Confirm API access-control configuration.
5. Determine whether the 403 originated from the gateway or backend.

Resolution:
- Correct authorized scopes or roles through the approved access process.
- Fix incorrect authorization policy configuration.
- Do not bypass security policies to resolve the error.

## Scenario 3: HTTP 429 Too Many Requests

Platform: Axway API Gateway
Category: Traffic Management
Symptoms: API clients receive HTTP 429 responses.

Possible causes:
- API rate limit exceeded.
- Application quota exhausted.
- Unexpected request spikes.
- Client retry loops generating excessive traffic.

Troubleshooting:
1. Review API Gateway traffic-management policies.
2. Check configured rate limits and quotas.
3. Examine request volume and client identifiers.
4. Inspect Retry-After response headers if present.
5. Identify duplicate requests or aggressive retry behavior.

Resolution:
- Implement client-side backoff and respect Retry-After where provided.
- Reduce unnecessary requests and retry loops.
- Review rate limits with API owners before changing quotas.
- Monitor traffic after remediation.