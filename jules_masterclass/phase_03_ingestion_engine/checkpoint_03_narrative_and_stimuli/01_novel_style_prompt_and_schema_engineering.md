# Novel-Style Prompt and Schema Engineering

To force an LLM to output narrative-driven micro-chunks:
1. **Strict Pydantic Validation**: By using constraints like `ge=15, le=35` for `duration_seconds` and requiring an explicit `AVStimulusDirective`, the LLM is forced into the schema format.
2. **Tone Directives**: Replacing academic tone with a "mystery/discovery" loop inside the narrative prompt context.
3. **Bite-Sized Pacing**: Forcing scenes under 35 seconds ensures rapid dopamine loops, crucial for sustained attention.
