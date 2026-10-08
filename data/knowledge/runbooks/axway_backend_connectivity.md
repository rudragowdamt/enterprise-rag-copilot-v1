# Axway Backend Connectivity Failure
Document ID: RB-AXWAY-002
Platform: Axway API Gateway

## Symptoms
Connection refused, connection reset, DNS failure, TLS handshake error or intermittent backend connection errors.

## Checks
Validate backend hostname and port, DNS resolution, route/firewall path, TLS certificate chain, truststore, supported protocol/cipher configuration and backend listener health. Compare the failing node with another gateway node to isolate node-specific configuration.

## Recovery
Restore the dependency or configuration, then execute a controlled API request and confirm gateway and backend logs share the same correlation ID.
