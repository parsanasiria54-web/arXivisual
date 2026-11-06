# ADHD Cognitive Load and DAG Theory

## Intrinsic vs Extraneous Cognitive Load
Traditional top-down academic teaching inherently forces the learner's brain to manage extraneous cognitive load. When teaching a complex algorithm, authors often present the final concept first, assuming working memory can suspend "unknown variables" until they are later defined. This fails specifically for ADHD learners.

## The Bottom-Up Topological Solution
By converting the domain space into a Directed Acyclic Graph (DAG) and running Kahn's algorithm or DFS to perform a bottom-up topological sort, we build a mathematical guarantee: no concept is ever taught before its prerequisites exist in the learner's mental state. Level 0 nodes (axioms) are defined first, clearing working memory overhead.
