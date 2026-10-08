# Payment Integration Flow
Document ID: ARC-002
Service: PaymentService

## Flow
Client -> Axway API Gateway -> Payment Integration Service -> Payment Backend -> Payment Database

Authentication occurs at the API edge. Axway performs routing and policy enforcement. The Payment Integration Service transforms and validates the request before invoking the backend.

## Failure Interpretation
401 normally requires authentication/policy investigation. 504 requires latency/dependency tracing. A database bottleneck can manifest to the client as a gateway 504.
