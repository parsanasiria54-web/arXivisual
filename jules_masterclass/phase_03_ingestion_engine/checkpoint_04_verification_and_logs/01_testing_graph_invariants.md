# Testing Graph Invariants

Property-based testing is critical here.
- **Topological Validity**: After sorting, for any node $X$, its prerequisites must strictly precede $X$ in the returned list.
- **Cycle Catching**: Constructing an artificial loop (e.g. A->B->C->A) must robustly trigger exception paths.
- **Anchor Logic**: Testing that timelines inject a `working_memory_anchor` exactly when `distance > 2` ensures we are meeting cognitive offloading rules.
