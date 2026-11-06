# Deep Dive: The 70% Pedagogical Isomorphism Engine

## Philosophy
The core of effective CS pedagogy is ensuring the visual behavior on screen structurally matches the concept being taught.
This 70% engine strips away all aesthetics to focus strictly on these mechanics.

## Key Examples

### 1. Base-N Place-Value Overflow Bundling
When teaching Base-10 or Base-2, the transition isn't just a number changing on a screen. It must physically show 10 individual units collapsing into 1 bundle, and migrating left to a new column. This physical compression and migration *is* the concept. Our `generate_base_n_bundling` generates the exact style-agnostic entities and `bundle_and_shift` transitions for this.

### 2. Pointer Kinematics
In a Linked List, an insertion requires a pointer detaching from its current target and swinging to point at a new one. `generate_pointer_relinking` encapsulates this semantic. It outputs pure states: "pointer detached" and "pointer attached".

By isolating these physical transitions from how they look, we guarantee that the educational content is never compromised by the aesthetics.
