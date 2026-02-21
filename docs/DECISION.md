# Architecture Decision Records

## ADR-001: Keep `get_key_value_list()` and `remove_element()` separate

**Date:** 2026-02-21
**Status:** Decided

### Context

Both functions recursively traverse nested dict/list structures using dotted paths:

- `get_key_value_list()` in `src/roadmap_app/utils.py` — flattens the entire structure into a key-value list
- `remove_element()` in `src/roadmap_app/model.py` — deletes elements at a specific path

Shared patterns: `isinstance` checks on list/dict, recursive calls, hierarchical dotted paths.

However, their traversal strategies differ significantly:

| Aspect | `get_key_value_list()` | `remove_element()` |
|--------|----------------------|-------------------|
| Purpose | Collect all leaves | Delete at target path |
| Traversal | Exhaustive (all paths) | Targeted (follow one path) |
| Path construction | Bottom-up (prefix grows) | Top-down (split + consume) |
| Return | List of `{key, value}` | In-place mutation |

### Decision

**Keep both functions as-is.** No refactoring of the shared traversal logic.

### Rationale

- Traversal strategies differ fundamentally (exhaustive vs. targeted, bottom-up vs. top-down)
- A shared helper would need to support both modes, making the abstraction more complex than the duplication it eliminates
- Duplication is manageable (~40 lines per function)
- YAGNI — revisit if a third traversal function is needed

### Rejected Alternatives

- **Shared Traversal Helper:** Traversal strategies are too different for a meaningful shared abstraction
- **Visitor Pattern:** Over-engineering for two functions
