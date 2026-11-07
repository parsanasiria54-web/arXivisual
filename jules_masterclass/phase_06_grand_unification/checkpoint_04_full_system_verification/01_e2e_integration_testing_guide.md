# E2E Integration Testing Guide

End-to-End testing verifies the grand unification of all modules.

## Strategy
Tests should invoke the orchestrator pipeline with mock inputs and verify that the final output state matches the expected schema.

## Execution
Run integration tests using the `Run-AllMasterclassTests.ps1` script, which aggregates testing across all modules using `pytest`.
