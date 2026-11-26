# Completion

Accepted on 2026-11-26 for ygoDocGen v2.0.0.

The standard-library Python CLI regenerates DataEditorX Lua API signatures
from the five ocgcore binding sources, merges handwritten annotations and
exports field-level source evidence as JSON. The original script and its
published example are retained in the legacy reference.

## Reproduce

Use Python 3.9 or 3.14 and a separate checkout of the
[ocgcore reference revision](https://github.com/Fluorohydride/ygopro-core/tree/2e47dbead97c3826d2f0779ed3ccb78fde772866).
From this repository, run these commands with that checkout's path.

```sh
python3 ygoDocGen.py --dir /path/to/ocgcore --check
python3 ygoDocGen.py --dir /path/to/ocgcore --annotations new_functions.txt --json api.json > api.txt
YGODOCGEN_CORPUS=/path/to/ocgcore python3 -m unittest discover -s tests -q
```

Independent validation passed 41 tests in each combination of Python 3.9
and 3.14 with ocgcore revisions `2e47dbe` and `7bd9ef6`. The reference
revision yielded 611 Lua registrations, 79 yielding bindings and zero
structural defects. The newer tested revision yielded 616 registrations.
The checked-in annotations include 591 qualified blocks, of which 548
match a binding at the reference revision. See the [README](README.md)
for the measured scope and examples.

Three argument types are unreadable from the tested C++ bodies and are
reported as unknown. Ordinary `--check` accepts those warnings.
`--check --strict` returns 1 on those same sources.
