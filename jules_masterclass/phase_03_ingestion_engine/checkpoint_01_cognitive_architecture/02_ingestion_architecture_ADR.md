# Ingestion Architecture ADR

## Decision
We abstract all input modalities (arXiv, PDF, Markdown, Topic string) into a unified `IngestionSource` contract.

## Pipeline Diagram (Mermaid representation)
```mermaid
graph TD
    A[Raw Source: PDF/arXiv] -->|Extractor| B(Raw Text)
    B -->|Cognitive Decomposer| C(Concept Dependency DAG)
    C -->|Topological Sort| D(Ordered Atomic Concept Nodes)
    D -->|Narrative Weaver| E[Novel-Style Micro-Scene Manifest with AV Stimuli]
```
The architecture enforces Working Memory Anchor injections during the graph traversal to maintain low cognitive load.
