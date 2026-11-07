# Dynamic Plugin Architecture

This document describes the design of our dynamic plugin architecture used for wiring the pipeline components together.

## Defensive Dynamic Mounting
To allow for isolated testing and development of individual components, the orchestrator uses `importlib` to dynamically load modules (`backend.core_ingestion`, etc.).

If a module is not found, the orchestrator defaults to a mock implementation, allowing the rest of the pipeline to run uninterrupted. This is crucial for avoiding blocking errors during partial builds.
