# Orchestrator ADR (Architecture Decision Record)

## Context
We need a central orchestrator to manage the end-to-end cognitive pipeline across multiple modular components (ingestion, pedagogy, TTS, rendering).

## Decision
We will implement an event-driven orchestrator using Python's `asyncio` and `importlib` for defensive, dynamic module loading. State will be managed using Pydantic models.

## Consequences
- **Positive:** High resilience. If one module is missing or fails, the orchestrator can mock or gracefully degrade.
- **Negative:** Increased complexity in debugging dynamic imports compared to static imports.
