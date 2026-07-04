# Entity Resolution Gate

This layer prevents NEXUS from splitting compound terms too aggressively.

Example:

Bad:
- 東京造形 -> 東京 + 造形

Good:
- 東京造形 -> likely 東京造形大学

## Priority

1. Exact alias
2. Possible proper noun
3. General knowledge
4. Clarification
5. Search if available
