# Domain Layer

This layer contains business logic and financial invariants.

It must not:
- Import FastAPI
- Perform HTTP calls
- Construct raw SQL
- Depend on infrastructure details

The domain layer orchestrates workflows and enforces financial rules.
