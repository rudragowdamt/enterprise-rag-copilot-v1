---
title: Digital Commerce Service Dependency Map
doc_type: architecture
system: DigitalCommerce
environment: PROD
---
CheckoutService calls IdentityService for authentication and PaymentAPI for payment initiation. PaymentAPI calls PaymentGateway and LedgerService. OrderService persists orders to OrderDB and publishes order events. IdentityService is therefore a direct dependency of CheckoutService and an indirect dependency of authenticated checkout flows.
