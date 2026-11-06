# DAG Topological Sorting Guide

## Overview
Topological sorting maps directly to prerequisite-driven learning.

1. **Cycle Detection**: Using Kahn's algorithm, if the visited nodes count does not match the total node count, there is a circular dependency (e.g., A needs B, B needs A). This throws a `CycleDetectedException`.
2. **Bottom-Up Grouping**: Roots (in-degree 0) start at Level 0. As we process neighbors, we assign them `max(levels[neighbor], levels[curr] + 1)`.
3. **Working-Memory Anchors**: As we walk the timeline, we check the distance between the current scene index and a prerequisite's introduction index. If `distance > 2`, we inject a visual reminder to prevent cognitive drop.
