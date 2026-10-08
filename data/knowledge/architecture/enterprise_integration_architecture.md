# Enterprise Integration Platform Architecture
Document ID: ARC-001

The fictional Acme Enterprise integration estate uses multiple integration technologies. Boomi supports SaaS/application and batch integrations. Axway API Gateway exposes selected partner and external APIs. Layer7 API Gateway protects internal and customer-facing APIs with authentication and policy enforcement. SFTP supports legacy partner file exchange. Integration services depend on identity providers, databases, ERP/CRM platforms and downstream microservices.

## Operational Principle
Troubleshooting must follow the transaction across layers. A gateway error does not automatically mean the gateway is the root cause.
