# YGOPro Documentation Generator

**Completed v2.0.0.** The evidence-backed DataEditorX Lua API generator is complete for the documented scope. See [completion and verification](COMPLETION.md).

Regenerate the `DataEditorX` Lua API document from the real `ocgcore` binding
sources. One file, `ygoDocGen.py`, Python 3 standard library only, runnable
from any directory. Every signature it prints comes from a statement in the
C++ sources, and `--json` hands you the statement behind each field.

**中文摘要**：这是只依赖 Python 标准库的生成器，从 ocgcore 的 C++ 绑定源码重新生成
DataEditorX 用的 Lua API 文档。每条签名都能追溯到源码里的具体证据（注册表、
`check_param_count`、栈读取、push、手写注释），`--json` 逐字段给出证据原文。
旧版脚本已移入 `legacy/`，按原样运行会失败（实测见下）；另一套解析器
`ygodoc.py` 也无法替代它（实测对照见下）。

```console
$ python3 ygoDocGen.py --dir path/to/ygopro-core > api.txt        # generated only
$ python3 ygoDocGen.py --dir path/to/ygopro-core \
                       --annotations new_functions.txt > api.txt  # with the 591 Chinese blocks
```

Output starts like this (`--dir <pinned checkout>`, verbatim, first five lines):

```
●int Card.GetCode(card pcard)
●int Card.GetOriginalCode(card pcard)
●int Card.GetOriginalCodeRule(card pcard)
●int... Card.GetFusionCode(card pcard)
●int... Card.GetLinkCode(card pcard)
```

# What it does

* Walks the five binding sources (`libcard.cpp`, `libduel.cpp`, `libeffect.cpp`,
  `libgroup.cpp`, `libdebug.cpp`). It looks in the directory you give it, in
  `ocgcore/`, `src/`, `ygopro-core/`, and anywhere below that directory; when
  several layouts exist it reads the most complete one and says so on stderr
  rather than documenting a partial copy.
* Reads the Lua name and namespace from the `luaL_Reg` tables and the
  `lua_setglobal` call, never from the C symbol. `scriptlib::card_get_origin_code`
  is `Card.GetOriginalCode`; nothing has to guess that.
* Infers argument and return types from the body: `check_param`,
  `check_param_count`, `lua_to*`, `*(card**)lua_touserdata`, `lua_gettop`,
  `lua_isnil` guards, the `push*` calls, and the continuation passed to
  `lua_yieldk`. A callee with a literal `return N` gives the caller that count.
* Merges the hand-written Chinese blocks when you pass `--annotations`. An entry
  with a block is printed exactly as its author wrote it; the rest are
  generated. Blocks with no binding (`aux.*` helpers) are kept at the end under
  their own heading, never dropped.
* Refuses to lie about coverage: a missing library file is reported on stderr,
  counted as a defect by `--check`, and recorded in the JSON as
  `missing_sources`.

It does not read Lua scripts, does not evaluate C++ expressions, and does not
invent a type to fill a gap: what the body does not show stays `?` and is listed
by `--check`.

# Read the output

Every row below quotes a real `●` line from that same generated document in
full, from wherever it occurs — they are not consecutive, and only the
explanations are written for this table. A test keeps them verbatim.

| piece | meaning | real example |
| --- | --- | --- |
| `●` | start of an entry, as in `DataEditorX`'s `_functions.txt` | |
| `int,int` | exactly two values | `●int,int Card.GetUnionCount(card pcard)` |
| `int\|effect...` | one value per result, `int` or `effect` | `●int\|effect... Card.GetSpecialSummonInfo(card pcard, int flag...)` |
| `int...` | one value per result; the count is not fixed — see `Known limits` for which side decides it | `●int... Card.GetFusionCode(card pcard)` |
| `~int` | yields: a value arrives only when the coroutine resumes | `●~int Card.RemoveOverlayCard(card pcard, int playerid, int min, int max, int reason)` |
| `[nil\|int cp]` | argument may be omitted, or passed as nil | `●int Card.GetLinkedZone(card pcard, [nil\|int cp])` |
| `int tcode...` | tail taking zero or more `int` values | `●bool Card.IsFusionCode(card pcard, int tcode...)` |
| `~int...` | yields, and then one value per result | `●~int... Duel.TossCoin(int playerid, int count)` |
| `...` | variadic tail whose element type the body never reveals | `●group Duel.GetMatchingGroup(function, int self, int location1, int location2, nil\|card\|group pexception, ...)` |
| `?` | nothing readable in the body; reported by `--check` | `●bool Duel.IsChainNegatable(?)` |
| bare `function`, `int` | the source never names that argument | `●~int Duel.DiscardHand(int playerid, function, int min, int max, int reason, [nil\|card\|group pexception], ...)` |

Generated entries are one `●` line. With `--annotations` the author's text is
reproduced verbatim, so an annotated entry may still use the looser old style
(`[int,int]` for an absent second value, `card pcard` for a typed argument).
That is deliberate: those 591 blocks are what `DataEditorX` already ships, and
`new_functions.txt` is their authority, not this tool. Use `--mark` to label
each generated entry (` (generated from libcard.cpp; no hand-written
description)`), so a reader can tell which text came from a person.

# Where each field comes from

| field | authority in the sources |
| --- | --- |
| Lua name, namespace | `luaL_Reg cardlib[] = { {"GetOriginalCode", scriptlib::card_get_origin_code}, ... }` and `lua_setglobal(L, "Card")` |
| required count | `check_param_count(L, N)`, or `lua_gettop(L) - k` |
| argument types | `check_param(L, PARAM_TYPE_CARD / INT / ...)`, `lua_tointeger/tonumber/toboolean/tostring`, `*(card**)lua_touserdata(L, i)` |
| optional arguments | `if(lua_gettop(L) >= k && !lua_isnil(L, k))` guards |
| return shape | `lua_push*`, `interpreter::card2value/group2value`, a callee's literal `return N`, the `lua_yieldk` continuation |
| description | the hand-written `●` block from `--annotations` |

Each of those lands in the record: `args[i].evidence`, `min_evidence`,
`return_evidence`, `notes`, `return_arity_cause`. The whole record for the entry
that was already explained above, quoted from `--json` in full (whitespace
reflowed to fit; a test parses this block and compares every field with the live
output, so it cannot drift):

```json
{"name": "Card.GetLinkedZone", "lua_name": "GetLinkedZone", "namespace": "Card",
 "symbol": "card_get_linked_zone", "table": "cardlib", "table_index": 36,
 "file": "libcard.cpp", "required": 1,
 "min_evidence": "check_param_count(L, 1)",
 "args":
  [{"position": 1, "type": "card", "optional": false, "variadic": false,
    "name": "pcard",
    "evidence": ["card* pcard = *(card**) lua_touserdata(L, 1);",
                 "check_param(L, PARAM_TYPE_CARD, 1);"]},
   {"position": 2, "type": "nil|int", "optional": true, "variadic": false,
    "name": "cp",
    "evidence": ["cp = (int32_t)lua_tointeger(L, 2);",
                 "if(lua_gettop(L) >= 2 && !lua_isnil(L, 2))"]}],
 "return": "int", "return_count": 1, "return_arity": "fixed",
 "return_arity_cause": null,
 "return_evidence": ["lua_pushinteger", "return 1;"],
 "yields": false, "issues": [], "notes": []}
```

A record whose arity is not fixed says why, instead of printing a count it
cannot know. `Duel.GetChainInfo`, shortened to the fields involved (also
compared with the live record by the suite):

```json
{"name": "Duel.GetChainInfo",
 "return": "int|group|effect...", "return_count": null,
 "return_arity": "input-dependent", "return_arity_cause": "arguments",
 "return_evidence": ["derived: the count is `args`, the number of extra arguments (`lua_gettop(L) - 1`)",
                     "interpreter::effect2value",
                     "interpreter::group2value",
                     "lua_pushinteger",
                     "lua_pushnil",
                     "return args;"]}
```

`derived:` is the second kind of evidence, and the only one you cannot find by
searching the file: everything else in `evidence` is a statement quoted from the
named source (whitespace collapsed), while a `derived:` string is the tool's own
reasoning about those statements. The suite checks that promise over the whole
corpus: every unprefixed string must occur in the file the record names.

# Measured results

On the checkout pinned at commit `2e47dbead97c3826d2f0779ed3ccb78fde772866` of
`Fluorohydride/ygopro-core` (the six files this repo was built against):

```console
$ python3 ygoDocGen.py --dir <pinned checkout> --check
functions: 611
  libcard.cpp    Card     276 registrations
  libduel.cpp    Duel     229 registrations
  libeffect.cpp  Effect    55 registrations
  libgroup.cpp   Group     40 registrations
  libdebug.cpp   Debug     11 registrations
yielding: 79   unknown fields: 3   defects: 0   warnings: 3

warnings (inferred as ?):
  libduel.cpp:duel_is_chain_negatable: argument 1 has no readable type
  libdebug.cpp:debug_message: argument 1 has no readable type
  libdebug.cpp:debug_show_hint: argument 1 has no readable type
```

* 611 registrations over 609 function bodies: `group_get_count` is registered
  twice (`GetCount`, `__len`) and `group_meta_add` twice (`__add`, `__bor`).
* Zero defects: every registration has a definition, no Lua name is duplicated,
  no symbol contradicts its namespace, no source file is missing.
* Three honest warnings, all one shape — an argument the body never reads:
  `Duel.IsChainNegatable` arg 1, `Debug.Message` arg 1, `Debug.ShowHint` arg 1.
* 79 bindings yield.

**The counts belong to that commit, not to the tool.** Upstream HEAD `7bd9ef6`
has 616 registrations: five added in `Card` (`GetCardType`,
`GetPreviousCardTypeOnField`, `IsAllCardTypes`, `IsCardType`,
`IsPreviousCardTypeOnField`), none removed, and `Debug.PreAddCounter` gained an
optional 3rd argument (`nil|int`) because the source grew an
`if(lua_gettop(L) >= 3)` guard. Zero defects, three warnings and 79 yielding
hold there too.

What the suite promises depends on which checkout you point it at, and that is
deliberate: **every number, example line and JSON sample in this README is a
fact about the revision named above.** On that revision the suite asserts them
exactly. On any other checkout it asserts only what a newer revision cannot
invalidate: the five tables are found, names match them one-to-one, the total equals the sum of
the per-library counts, `--check` reports zero defects, every `●` line quoted
here still names a binding the checkout has, and the JSON sample keeps the same
keys and identity. You then get the real composition printed on stderr:

```console
note: <checkout> is not the pinned revision; 616 registrations (Card 281, Duel 229, Effect 55, Group 40, Debug 11)
```

So pointing the tool at newer sources is a supported, tested action; it just
must not claim this README's counts for them.

With `--annotations new_functions.txt` (gb18030 + CRLF, as found in the repo):

| | count |
| --- | --- |
| annotation blocks read | 591 |
| matched to a binding, emitted verbatim | 548 |
| bindings with no block, printed generated | 63 |
| stale C++-derived line inside a block, dropped | 490 |
| blocks with no binding, kept at the end | 43 |

1505 lines, 654 `●` lines on the pinned revision. The one block without a
signature (`void initial_effect(Card c)`, a file header) is reported on stderr,
not guessed at. A test re-runs this merge and compares every number above with
the live result, so the table cannot go stale unnoticed; on another checkout it
reports the counts it measured instead of failing, since `new_functions.txt` is
described against the pinned revision.

# About `ygodoc.py` — it cannot replace this repo

A second, 84-line generator elsewhere also calls itself `ygodoc.py`. Measured
on the same pinned checkout, against the same tables (`interpreter.cpp` +
`luaL_Reg`):

| | this tool | `ygodoc.py` |
| --- | --- | --- |
| bindings printed | 611 of 611 | 609 lines; 93 bindings never printed (`Group.__len`, `__add`, `__bor`, `__sub`, `__band`, `__bxor`, `Duel.CreateGroup`, …) |
| names that are real bindings | 611 | 518; 91 printed names match no registration (`GetOriginCode` vs `GetOriginalCode`, `GetFieldid` vs `GetFieldID`, `GetOriginAttack` vs `GetBaseAttack`, `ChangeForm` vs `ChangePosition`, …) |
| stable across `PYTHONHASHSEED` 0/1/12345 | identical text and JSON | three different outputs |
| hand-written Chinese blocks | 548 merged verbatim | none |

Its names come from the C symbol with the underscore removed and the case
adjusted, which is why `card_get_origin_code` becomes `GetOriginCode` while a
Lua script types `GetOriginalCode`. Those numbers are a contrast, not the
standard: the `luaL_Reg` table of the checkout is the acceptance authority here,
and the suite re-derives the tables independently of the tool's own parse.

# The previous generator, in `legacy/`

`legacy/ygoDocGen_v1.py` is the script this README used to describe. Run on a
clean checkout exactly as it documents, it fails before printing a line:

```console
$ cd <ocgcore checkout> && python3 ../legacy/ygoDocGen_v1.py
Traceback (most recent call last, line 109, in <module>)
    old = re.sub('===+[^=]*=*\n', '', open('_functions.txt',encoding='utf-8-sig').read())
NameError: name 're' is not defined. Did you forget to import 're'?
```

It also wants `_functions.txt` from `DataEditorX`, which this repo never
shipped, and it only recognises the pre-table `scriptlib::card_get_code(lua_State*)`
registration style — on current sources its regexes match no registrations at
all. It is kept for provenance: `docs/reference-legacy-output.md` holds its
"Example Output" section byte for byte, which is the regression reference for
the 591 blocks. Don't maintain both — everything it produced is either
reproduced here or wrong.

# Verify

```console
$ python3 ygoDocGen.py --dir <checkout> --check           # exit 0, three warnings
$ python3 ygoDocGen.py --dir <checkout> --check --strict  # exit 1: those three are `?`
$ python3 -m unittest discover -s tests                   # 41 tests
```

On the pinned checkout `--check` returns 0 with three warnings and
`--check --strict` returns 1, which is the honest difference: nothing is
defective, but three argument types are still unknown. `--strict` is only read
by `--check`; alone it exits 2 with an error instead of printing a document that
looks verified.

Runs on Python 3.9 and 3.14. Measured on 3.14.10 and on 3.9.25: the
suite passes and the generated text and JSON are byte-identical across both.

Windows and any console whose code page cannot encode `●`: the document is
still written, as UTF-8, and one line on stderr says so. Redirecting inside
`cmd.exe` (code page 1252) previously ended the run at the first entry, after
the `--json` file had already been written. For a readable console, use
`python -X utf8 ygoDocGen.py ...` or set `PYTHONIOENCODING=utf-8`. A code page
that has the character (cp936) is left alone, so Chinese consoles are
unchanged. Measured: `PYTHONIOENCODING=cp1252` and UTF-8 produce byte-identical
documents in both modes.

The suite builds its own synthetic checkout with the expected answers written
by hand. When a real checkout is findable it also re-checks the numbers above
against it, and skips only that part otherwise. It looks at `YGODOCGEN_CORPUS`,
then at `ocgcore/`, `src/`, `ygopro-core/`, `ygopro-core/ocgcore/` in this
directory and beside it, so a clean copy needs no configuration:

```console
$ YGODOCGEN_CORPUS=/path/to/ygopro-core python3 -m unittest discover -s tests
```

Exit codes: `0` success; `1` a defect, or a warning under `--check --strict`,
or a render error (nothing is written then and the previous document stays
intact); `2` no binding sources at all, or `--strict` given without `--check`.

# Files

| path | what it is |
| --- | --- |
| `ygoDocGen.py` | the generator; the only code you need to run |
| `legacy/ygoDocGen_v1.py` | the previous generator, unmodified, does not run |
| `new_functions.txt` | the 591 hand-written blocks, gb18030 + CRLF; keep the encoding |
| `docs/reference-legacy-output.md` | the old tool's output, preserved verbatim |
| `tests/test_ygodocgen.py` | the suite (41 tests); synthetic fixture first, real sources when available |

# Known limits

* `check_param(L, PARAM_TYPE_*, n, TRUE)` means "nil is accepted". That is
  inferred from all five sources, not from `check_param` itself, whose header is
  not part of this checkout.
* 104 of 1356 arguments have no name in the sources (`pcard->unique_pos[0] =
  (uint8_t)lua_tointeger(L, 2)`), so they are printed by type only.
* Ten bindings have a return count that is not fixed
  (`Card.GetFusionCode` hands back one value per "code" on the card,
  `Duel.GetChainInfo` one per extra argument, `Duel.TossCoin` one per coin).
  They print `...`, and the JSON says which: `return_arity_cause` is
  `arguments` when the caller's arguments decide the count
  (`Duel.TossCoin`, `Duel.TossDice`, `Duel.GetActivityCount`, `Duel.GetChainInfo`,
  `Card.GetSpecialSummonInfo`) and `state` when the duel does
  (`Card.GetFusionCode`, `Card.GetLinkCode`, `Duel.GetFlagEffectLabel`,
  `Duel.GetFirstTarget`, `Duel.GetCoinResult`). The quoted statement the count
  comes from is in `return_evidence`.
* A body that reads a stack slot without a `check_param` or a cast gets a
  generated `?` type and a warning; the tool never guesses one. Three such
  arguments remain, all of them an argument the body genuinely never reads
  (`Duel.IsChainNegatable`, `Debug.Message`, `Debug.ShowHint`).
