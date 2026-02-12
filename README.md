# FastAPI Fintech Application

## Purpose

This repository contains a production-oriented fintech web application built with FastAPI.

The application consumes a custom Elixir-based RDBMS over a network boundary.  
It treats that database as a black-box service and never bypasses its public HTTP interface.

This project exists to demonstrate:

- Explicit architectural boundaries
- Correct handling of distributed systems concerns
- Security-first backend engineering
- Clear separation of concerns
- Documented trade-offs and limitations
- Production-grade discipline in structure and reasoning

This is an educational project. It is not a toy.

---

# System Boundary (Non-Negotiable)

## The Elixir RDBMS Owns

- Data persistence
- Concurrency
- Constraint enforcement
- Atomic execution of single SQL statements
- Transactional guarantees provided internally
- Table storage and indexing
- Low-level correctness

The database exposes a narrow HTTP API for executing SQL statements.

## This FastAPI Application Owns

- HTTP API surface
- Authentication and authorization
- Request validation
- Domain workflows (payments, merchants, settlements)
- Idempotency handling
- Error translation
- Security enforcement
- Observability
- Business invariants
- Auditability
- Multi-step workflow orchestration

The application does not:
- Access disk storage directly
- Bypass SQL execution
- Inspect database internals
- Re-implement database constraints
- Enforce primary keys
- Manage database transactions internally

If database logic appears in the application layer, that is a design failure.

---

# Architecture Overview

The system is layered and strictly directional:

    API Layer
    ↓
    Domain Layer
    ↓
    Infrastructure Layer (DB Client)
    ↓
    External Elixir RDBMS (Network Boundary)


No layer may reach upward.
No circular dependencies are allowed.

## API Layer

Responsibilities:
- Define HTTP routes
- Validate request schemas
- Authenticate and authorize
- Map domain results to HTTP responses

It contains no business logic.

## Domain Layer

Responsibilities:
- Business rules
- Financial invariants
- Idempotency semantics
- Workflow orchestration
- Multi-step operations

It does not:
- Construct SQL directly
- Perform HTTP calls
- Depend on FastAPI

## Infrastructure Layer

Responsibilities:
- Database client implementation
- HTTP calls to Elixir RDBMS
- Retry handling
- Timeout management
- Structured logging

It does not:
- Contain business logic
- Make authorization decisions
- Perform request validation

## Security Layer

Responsibilities:
- Authentication mechanisms
- Token validation
- Role-based access enforcement
- Merchant isolation rules

Security rules are explicit and testable.

## Configuration Layer

Responsibilities:
- Environment parsing
- Service configuration
- Fail-fast startup validation

---

# Consistency & Concurrency Model

This application relies on the Elixir RDBMS for atomic execution of single SQL statements.

### Atomic Operations

Any single SQL execution sent to the database is considered atomic within the database.

### Non-Atomic Operations

Multi-step workflows (e.g., create payment → update balance → create ledger entry) are not atomic at the application layer.

These require explicit orchestration and must handle:

- Partial failures
- Retry logic
- Idempotency keys
- Compensating actions where appropriate

### Race Conditions

Race conditions are mitigated by:

- Relying on database-level atomicity
- Designing idempotent write operations
- Avoiding read-modify-write cycles when possible
- Using invariant-preserving SQL patterns

The BEAM runtime inside the Elixir database provides concurrency isolation internally. The application assumes no shared memory concurrency with the database.

---

# Security Model

The application will implement:

- JWT-based authentication
- Role-based authorization
- Merchant-level isolation
- Input validation on all endpoints
- Safe SQL generation
- Structured audit logging for financial actions
- Error translation to prevent information leakage

Threats considered:

- SQL injection
- Horizontal privilege escalation
- Replay attacks
- Double-spend attempts
- Denial of service via repeated writes
- Information disclosure via error messages

Rate limiting will be explicitly documented when implemented.

---

# Observability

The system will include:

- Structured logging
- Correlation IDs
- Database call tracing
- Audit logs for financial operations
- Explicit error categorization

Logs must never leak secrets.

---

# Testing Philosophy

Tests demonstrate correctness, not coverage percentages.

The test suite will include:

- Domain logic unit tests
- Integration tests against the database service
- Security enforcement tests
- End-to-end payment lifecycle tests
- Failure-mode tests (timeouts, partial failures)

Correctness is defined as preservation of financial invariants and isolation guarantees.

---

# Known Limitations

- Distributed multi-step transactions are not atomic.
- Network failures may cause partial execution of workflows.
- The database API contract defines the system’s durability and consistency characteristics.
- This system does not attempt to re-implement distributed transaction protocols.

---

# Development Principles

- Documentation precedes implementation.
- Every commit explains intent.
- No hidden coupling.
- No speculative abstraction.
- No premature optimization.
- Clear boundaries over clever tricks.

---

# AI Usage Transparency

AI may be used as a drafting tool.

All architectural decisions, reasoning, and final code are human-reviewed and intentional.

---

# Running (Future)

Setup instructions will be added once the application bootstrapping is implemented.

This initial commit establishes boundaries and architecture only.



# Configuration Model

Configuration is treated as a first-class boundary.

The application must fail fast on invalid or incomplete configuration.

No implicit defaults are allowed for security-sensitive values.

## Required Environment Variables

APP_ENV
    development | staging | production

APP_PORT
    Integer. Port for HTTP server.

DB_BASE_URL
    Base URL of Elixir RDBMS HTTP API.

DB_TIMEOUT_SECONDS
    Positive integer.

JWT_SECRET
    Non-empty string. Must not use default value in production.

JWT_ALGORITHM
    Must match supported algorithm list.

## Startup Validation

At startup:

- All required variables must exist.
- Values must pass validation constraints.
- Production mode must reject insecure defaults.
- Configuration is immutable after load.

If validation fails, application must terminate.

Rationale:

Fintech systems must never run in partially configured states.

## Environment Variable Loading

The application reads configuration exclusively from process
environment variables.

### `.env` Files

`.env` files are supported **only in development and test environments**
as a local developer convenience.

They are **not** used in production.

Rationale:
- Production systems must not depend on filesystem-based secrets
- Environment variables are the explicit configuration boundary

If `.env` support is removed or misconfigured, the application must fail
fast at startup.




---

## Domain Model Overview

The domain layer models financial concepts independently of:

* HTTP transport
* Database representation
* SQL schema
* Authentication mechanisms

It defines:

* Core entities (Merchant, Payment, LedgerEntry)
* Value objects (Money, Currency)
* Domain invariants
* State transitions

The domain layer must not:

* Call the database
* Construct SQL
* Import FastAPI
* Depend on infrastructure modules

All persistence concerns are external to the domain.

---

## Financial Modeling Principles

1. Money is represented using integers (minor units).
2. Currency is explicit.
3. Payment states are finite and explicit.
4. Balances are derived from ledger entries.
5. Domain logic must be deterministic and side-effect free.

Rationale:

Financial correctness depends on eliminating ambiguity in state transitions and monetary representation.

---



















































































