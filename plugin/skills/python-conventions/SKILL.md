---
name: python-conventions
description: The owner's Python conventions - Google docstrings, type hints, PEP 8 names, no import-time side effects, lock files, English in code, stdlib logging. Use when writing or reviewing Python code in any project.
---

# Python conventions

Defaults with reasons, walked with the owner (`<brain>/_harness/decisions.md`, 2026-11-27). A project's decisions
file overrides them.

## Docstrings: Google style

- Summary on the first line, one line, ending with a period. Then `Args:`, `Returns:` (`Yields:`), `Raises:`.
- With type hints, leave types out of the docstring; without them, put the type in parentheses.
- Where a caller can fall into a trap, say so on a `Warning:` line in the docstring.
- Every module starts with a docstring saying what it is for. Classes list public attributes under `Attributes:`.

```python
def get_test_loader(dataset: DatasetChoice, batch_size: int, size_filter: int) -> DataLoader:
    """Build a loader over a whole dataset, without a train/val/test split.

    Warning: use only on datasets the model has not seen. size_filter must match training.

    Args:
        dataset: Which dataset to load.
        batch_size: Samples per batch.
        size_filter: Largest image side kept, in pixels; larger images are dropped.

    Returns:
        A loader that yields (image, target, thumb, label) tuples.
    """
```

## Type hints

On public functions and methods; private helpers optional. Tensor shapes don't fit in hints: keep them in the
docstring or a comment (`# (B, 1, H, W) -> (B, 32, H, W)`).

## Names (PEP 8)

Lowercase module files (`skeview.py`, not `SkeView.py`), CapWords classes, `lower_with_under` functions and
variables, `UPPER_CASE` constants. Counts are `num_x` or `n_x` (`no_epochs` reads as "no epochs").

## Nothing runs at import

Parse arguments, pick devices, open files and print inside `main()` or a function, not at module level. Importing a
module runs its top-level code, so a module-level `parse_args()` makes pytest and notebooks exit on import.

## Dependencies

Each project keeps a lock file: `uv.lock` (preferred: `uv add <pkg>`) or a fully pinned `requirements.txt`. PyTorch
with CUDA needs its index set up once; run `/harness:library-check` the first time.

## Language

Identifiers, docstrings and comments in English, unless the project's CLAUDE.md opts out. Flag non-English slips
when reviewing the owner's code.

## Logging

- Each module: `logger = logging.getLogger(__name__)`.
- The entry point configures handlers once: console, plus a log file in the run's output folder.
- `print()` only for a command-line tool's ordinary output. `logger.info()` for progress, `logger.warning()` or
  `warnings.warn()` for warnings, raise an exception for errors (Python logging HOWTO, "When to use logging").
- Pass values as arguments, not f-strings: `logger.info("epoch %d dice %.3f", epoch, dice)` (Google §3.10.1: the
  pattern stays queryable, and nothing is formatted for a disabled level).
