#!/usr/bin/env python3
"""Generate YGOPro/ocgcore Lua API documentation from the C++ binding sources.

The name of every documented function comes from the ``luaL_Reg`` table that
registers it, read together with the ``lua_setglobal`` call in the matching
``open_*lib`` function.  That table -- not the C++ symbol name -- is what a
script author actually types, so ``card_get_origin_code`` is documented as
``Card.GetOriginalCode``.

Argument and return types are inferred only from statements in the C++ body
(``check_param``, ``lua_tointeger``, ``*(card**)lua_touserdata`` ...) and every
record keeps the evidence it used; nothing is invented to fill a gap.  Unknown
types stay ``?`` and are reported by ``--check``.

Usage, from any directory::

    python3 ygoDocGen.py                       # find the sources and print docs
    python3 ygoDocGen.py --dir path/to/ocgcore # explicit source directory
    python3 ygoDocGen.py --annotations new_functions.txt
    python3 ygoDocGen.py --json out.json       # full records with evidence
    python3 ygoDocGen.py --check               # verify, non-zero exit on defects
    python3 ygoDocGen.py --check --strict       # also fail on fields left as `?`

``--annotations`` merges the hand-written Chinese descriptions: an entry that
has an annotation block is emitted verbatim from that file (so the existing
``DataEditorX``-compatible text survives untouched), and entries without one
are generated from the source.  Without the flag, output is pure generation.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

VERSION = "2.0.0"

LIB_FILES = ["libcard.cpp", "libduel.cpp", "libeffect.cpp", "libgroup.cpp", "libdebug.cpp"]
CORPUS_SUBDIRS = ["ocgcore", "src", "ygopro-core"]

# Lua type vocabulary, ordered the way the annotation file orders alternatives:
# the nilable part first, then the narrowest type.
TYPE_ORDER = ["nil", "void", "int", "num", "bool", "str", "function", "card", "group", "effect"]
UNKNOWN = "?"

# The entry marker DataEditorX expects.  U+25CF is missing from several single
# byte code pages, which is why setup_stdio() below exists.
MARKER = "\u25cf"

PARAM_TYPES = {
    "PARAM_TYPE_INT": "int",
    "PARAM_TYPE_FLOAT": "num",
    "PARAM_TYPE_BOOLEAN": "bool",
    "PARAM_TYPE_STRING": "str",
    "PARAM_TYPE_FUNCTION": "function",
    "PARAM_TYPE_CARD": "card",
    "PARAM_TYPE_GROUP": "group",
    "PARAM_TYPE_EFFECT": "effect",
}

READ_TYPES = {
    "lua_tointegerx": "int",
    "lua_tointeger": "int",
    "lua_tonumberx": "num",
    "lua_tonumber": "num",
    "lua_toboolean": "bool",
    "lua_tolstring": "str",
    "lua_tostring": "str",
}

CONVERSIONS = {
    "interpreter::card2value": "card",
    "interpreter::group2value": "group",
    "interpreter::effect2value": "effect",
    "interpreter::function2value": "function",
}

PUSHES = {
    "lua_pushinteger": "int",
    "lua_pushnumber": "num",
    "lua_pushboolean": "bool",
    "lua_pushlstring": "str",
    "lua_pushstring": "str",
    "lua_pushnil": "nil",
}

CAST_TYPES = {"card": "card", "group": "group", "effect": "effect", "function": "function"}

# Type names usable as local variables, for naming arguments from the source.
LOCAL_TYPES = {"int": "int", "int32_t": "int", "uint32_t": "int", "lua_Integer": "int",
               "int64_t": "int", "uint64_t": "int", "lua_Unsigned": "int",
               "double": "num", "float": "num", "lua_Number": "num", "bool": "bool",
               "const char": "str", "char": "str", "lua_CFunction": "function",
               "card": "card", "group": "group", "effect": "effect"}

SLOT_READ = re.compile(
    r"(check_param_count|check_param|check_filter|get_operation_value|"
    r"interpreter::get_function_handle|lua_to[^\W_]+|lua_is[^\W_]+)\s*\(")
USERDATA_CAST = re.compile(r"\(\s*([A-Za-z_]\w*)\s*\*\s*\*\s*\)\s*[^\W_]*(?:lua_touserdata|touserdata)")
PUSH_CALL = re.compile(r"(lua_push[^\W_]+|interpreter::[^\W_]+2value|lua_createtable)\s*\(")
LOOP_DECL = re.compile(r"(?m)\bfor\s*\(\s*(?:int[0-9_a-z]*|unsigned\s*int|unsigned|uint[0-9_a-z]*|size_t|lua_Integer)\s+(\w+)\s*=\s*(\w+)")
SIMPLE_ASSIGN = re.compile(r"(?m)^\s*(?:const\s+)?([A-Za-z_]\w*)\s*(?:\*\s*)?(\w+)\s*=\s*([^{};]+);")


class DocError(Exception):
    """A construct the tool could not classify."""


def type_key(t):
    return (TYPE_ORDER.index(t) if t in TYPE_ORDER else len(TYPE_ORDER), t)


def join_types(types):
    return "|".join(sorted(set(types), key=type_key))


def render_return(ret, count, arity):
    """Render a return shape: a fixed count, or `...` for a varying one.

    A trailing `...` means "one or more values of this shape, as many as the
    call produced"; a fixed count above one is comma separated.
    """
    if not ret or ret == UNKNOWN:
        return ret
    real = [k for k in ret.split("|") if k != "nil"]
    if not real:
        return "nil"
    if arity == "input-dependent":
        return join_types(real) + "..."
    if count and count > 1:
        return ",".join(real)
    return join_types(real)


# --------------------------------------------------------------------------
# Low-level C++ scanning
# --------------------------------------------------------------------------

BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT = re.compile(r"//[^\n]*")


def blank_noise(text):
    """Replace comments by spaces so braces, parens and keywords can be trusted.

    Length and newlines are preserved, so offsets stay valid for the original
    text and the evidence strings can be sliced out of it.
    """
    def keep_newlines(m):
        return re.sub(r"[^\n]", " ", m.group(0))

    return LINE_COMMENT.sub(keep_newlines, BLOCK_COMMENT.sub(keep_newlines, text))


def skip_literal(text, i):
    quote = text[i]
    j = i + 1
    while j < len(text):
        if text[j] == "\\":
            j += 2
            continue
        if text[j] == quote:
            return j
        j += 1
    return len(text) - 1


def match_pair(text, open_pos, open_ch, close_ch):
    depth = 0
    i = open_pos
    while i < len(text):
        c = text[i]
        if c in "\"'":
            i = skip_literal(text, i)
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise DocError("unbalanced %r at offset %d" % (open_ch, open_pos))


def split_args(text, open_paren):
    """Split the argument list of the call whose '(' is at *open_paren*."""
    close = match_pair(text, open_paren, "(", ")")
    items, depth, cur = [], 0, []
    i = open_paren + 1
    while i < close:
        c = text[i]
        if c in "\"'":
            end = skip_literal(text, i)
            cur.append(text[i:end + 1])
            i = end + 1
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        if c == "," and depth == 0:
            items.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    tail = "".join(cur).strip()
    if tail:
        items.append(tail)
    return items


STATEMENT_BREAK = ";{())\n"


def statement_text(text, offset, limit=110):
    """The whole statement around *offset*, whitespace-collapsed, maybe cut.

    Evidence quotes must start and end on statement boundaries so a reader can
    find the quoted code again: slicing a fixed window around the match cuts
    tokens in half (`"; car"`, `")lua_tointeger(L, 2); if(cp == 1 - pcard`).
    The scan therefore follows brackets, so `if(check_param(L,
    PARAM_TYPE_CARD, 1)) return;` comes out whole and the quote is not a
    fragment of a call.  Only an over-long statement is trimmed, on a word
    break, with a trailing `...`.
    """
    start = offset
    depth = 0
    while start > 0:
        c = text[start - 1]
        if c == ")":
            depth += 1
        elif c == "(":
            if depth:
                depth -= 1
        elif c in STATEMENT_BREAK and depth == 0:
            break
        start -= 1
    end = offset
    depth = 0
    while end < len(text):
        c = text[end]
        if c == "(":
            depth += 1
        elif c == ")":
            if depth:
                depth -= 1
        elif c in STATEMENT_BREAK and depth == 0:
            if c == ";":
                end += 1
            break
        end += 1
    piece = " ".join(text[start:end].split())
    if len(piece) <= limit:
        return piece
    cut = piece[:limit - 3]
    if " " in cut:
        cut = cut[:cut.rindex(" ")]
    return cut.rstrip(" ,") + "..."


DERIVED = "derived: "


def derived(text):
    """A statement *about* the sources, not a quote from them.

    Evidence is read by people deciding whether to trust a field, so the
    difference has to be visible: a quote can be searched for in the file, an
    inference ("the count is `args` because ...") cannot.  Everything the tool
    reasons out is marked with this prefix, and the test suite enforces that
    every unprefixed evidence string really occurs in the file it names.
    """
    return DERIVED + text


def call_at(body, match):
    """Argument list of the call whose name ends at *match.end()*."""
    return split_args(body, body.index("(", match.end() - 1))


def guard_statement(text, offset):
    """The `if(...)`/`while(...)` condition enclosing *offset*, quoted whole.

    `if(lua_gettop(L) >= 2 && !lua_isnil(L, 2))` is what makes an argument
    optional; quoting only `lua_gettop(L) >= 2` drops the half that says nils
    are accepted, and neither fragment can be found as written in the file.
    When the match is not inside such a condition, the enclosing statement is
    quoted instead.
    """
    # Walk left to the parenthesis that encloses the match.
    depth = 0
    i = offset
    while i > 0:
        c = text[i - 1]
        if c == ")":
            depth += 1
        elif c == "(":
            if depth:
                depth -= 1
            else:
                head = re.search(r"(\w+(?:\s+if)?)\s*$", text[:i - 1])
                if head is None:
                    break
                if head.group(1) in ("if", "while", "else if", "elseif"):
                    close = match_pair(text, i - 1, "(", ")")
                    quote = text[head.start(1):close + 1]
                    return " ".join(quote.split())
                break
        elif c in ";{}\n" and depth == 0:
            break
        i -= 1
    return statement_text(text, offset)


def mask_lambdas(body):
    """Blank lambda bodies: what they push happens after the coroutine resumes."""
    out = list(body)
    for m in re.finditer(r"\[\s*\]\s*\([^)]*\)\s*(?:->[^ {]*)?\s*\{", body):
        start = body.index("{", m.start())
        end = match_pair(body, start, "{", "}")
        for i in range(start, end + 1):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def find_returns(body):
    """Offsets of `return` statements outside nested blocks (lambdas/ifs)."""
    found = []
    depth = 0
    i = 0
    while i < len(body):
        c = body[i]
        if c in "\"'":
            i = skip_literal(body, i)
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif body.startswith("return", i) and (i == 0 or not (body[i - 1].isalnum() or body[i - 1] == "_")):
            if depth == 0:
                found.append(i)
            i += 6
            continue
        i += 1
    return found


def int_value(expr, consts):
    expr = expr.strip()
    if re.fullmatch(r"[0-9]+", expr):
        return int(expr)
    return consts.get(expr)


DECL_CONST = re.compile(
    r"(?m)^(?:const\s+)?(?:int|int32_t|uint32_t|lua_Integer)\s+(\w+)\s*=\s*([0-9]+)\s*;")


def const_map(clean):
    """Numeric constants at *file* scope, e.g. `static int k = 3;`.

    Declarations inside a function body are locals, not constants: a body's
    `uint32_t count = 0;` must never be substituted into an unrelated `count`.
    """
    consts = {}
    depth = 0
    i = 0
    for m in DECL_CONST.finditer(clean):
        while i < m.start():
            c = clean[i]
            if c in "\"'":
                i = skip_literal(clean, i) + 1
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            i += 1
        if depth == 0:
            consts[m.group(1)] = int(m.group(2))
    return consts


def resolve_index(expr, aliases, loop_vars):
    """Classify a Lua stack index expression.

    Returns ``("literal", n)`` for a fixed position (0 is the return area),
    ``("relative", n)`` for a negative offset from the top of the stack,
    ``("vararg", base)`` for ``loop + base`` (the variadic tail starts at
    *base*), ``("vararg", None)`` for a bare loop variable, and ``None`` when
    the expression is not understood.
    """
    expr = expr.strip()
    if not expr:
        return None
    value = int_value(expr, aliases)
    if value is not None:
        return ("literal", value)
    if re.fullmatch(r"-[\w ]+", expr):
        off = int_value(expr[1:], aliases)
        return ("relative", -off) if off is not None else None
    m = re.fullmatch(r"(\w)\s*\+\s*([\w ]+)", expr)
    if m and m.group(1) in loop_vars:
        base = int_value(m.group(2), aliases)
        return ("vararg", base) if base is not None else None
    m = re.fullmatch(r"([\w ]+)\s*\+\s*(\w)", expr)
    if m and m.group(2) in loop_vars:
        base = int_value(m.group(1), aliases)
        return ("vararg", base) if base is not None else None
    if expr in loop_vars:
        # A bare counter: the tail starts wherever the loop starts.
        return ("vararg", loop_vars[expr]) if loop_vars[expr] is not None else ("vararg", None)


def slot_index(body, match, aliases, loop_vars):
    args = call_at(body, match)
    if not args:
        return None, None, args
    candidates = args[1:] if len(args) > 1 else args
    for a in candidates:
        target = resolve_index(a, aliases, loop_vars)
        if target is not None:
            return target[0], target[1], args
    return None, None, args
# --------------------------------------------------------------------------
# Registration tables: the authority for Lua names
# --------------------------------------------------------------------------

LUALIB_TABLE = re.compile(r"luaL_Reg\s+(\w+)\s*\[\s*\]\s*=\s*\{")
LUALIB_ENTRY = re.compile(r'\{\s*"([^"]+)"\s*,\s*scriptlib::(\w+)\s*\}')
SETGLOBAL = re.compile(r'lua_setglobal\s*\(\s*L\s*,\s*"([^"]+)"\s*\)')
DEF_START = re.compile(
    r"(?m)^[ \t]*int32_t\s+scriptlib::(\w+)\s*\(\s*lua_State\s*\*\s*L\s*\)\s*\{")
HELPER_DEF = re.compile(
    r"(?m)^[ \t]*int32_t\s+scriptlib::(\w+)\s*\(\s*lua_State\s*\*\s*L\s*,\s*(\w+)\s+(\w+)\s*\)\s*\{")


class Lib:
    """One binding source file: namespace, registration table, definitions."""

    def __init__(self, path):
        self.path = path
        self.name = path.name
        raw = path.read_text(encoding="utf-8", errors="replace")
        self.raw = raw
        self.clean = blank_noise(raw)
        self.namespace = None
        self.ns_evidence = None
        self.entries = []      # (lua_name, symbol, table, index)
        self.issues = []
        self.consts = const_map(self.clean)
        self.read_namespace()
        self.read_table()

    def read_namespace(self):
        m = re.search(r"(?m)^[ \t]*void\s+scriptlib::open_\w+lib\s*\(\s*lua_State\s*\*\s*L\s*\)\s*\{",
                      self.clean)
        if not m:
            return
        start = self.clean.index("{", m.end() - 1)
        end = match_pair(self.clean, start, "{", "}")
        g = SETGLOBAL.search(self.clean, start, end)
        if not g:
            self.issues.append("%s: open_*lib does not call lua_setglobal" % self.name)
            return
        self.namespace = g.group(1)
        self.ns_evidence = "%s: %s" % (self.name, self.clean[m.start():g.end()].splitlines()[0].strip()[:60])

    def read_table(self):
        for t in LUALIB_TABLE.finditer(self.clean):
            table = t.group(1)
            start = self.clean.index("{", t.end() - 1)
            end = match_pair(self.clean, start, "{", "}")
            for index, e in enumerate(LUALIB_ENTRY.finditer(self.clean, start, end), start=1):
                self.entries.append((e.group(1), e.group(2), table, index))
        if not self.entries:
            self.issues.append("%s: no luaL_Reg entries" % self.name)
            return
        prefix = None
        if self.namespace:
            prefix = self.namespace.lower() + "_"
        seen = {}
        for lua, sym, table, _ in self.entries:
            if lua in seen:
                self.issues.append("%s: Lua name %r registered twice (%s, then %s)"
                                   % (self.name, lua, seen[lua], sym))
            seen[lua] = sym
            if prefix and not sym.startswith(prefix):
                self.issues.append("%s: %r -> %s does not start with %r"
                                   % (self.name, lua, sym, prefix))


def find_libs(root):
    """Locate the binding sources under *root*.

    Returns ``(paths, missing, note)``.  ``missing`` lists the expected library
    files that were not found next to the ones that were: a partial checkout
    must be reported, never silently documented as if it were the whole API.

    Every plausible layout is searched -- *root* itself, the usual ``ocgcore`` /
    ``src`` / ``ygopro-core`` subdirectories, and any directory below the root
    holding a ``libcard.cpp`` -- and the *most complete* set wins.  Taking the
    first directory that has any file at all would let a stray partial copy
    beside a full checkout shrink the document without saying so; ``note``
    names the layout when the obvious answer was not the complete one.
    """
    candidates = [root] + [root / s for s in CORPUS_SUBDIRS]
    candidates += [p.parent for p in sorted(root.rglob("libcard.cpp"))]
    seen = []
    layouts = []
    for parent in candidates:
        if not parent.is_dir():
            continue
        try:
            key = parent.resolve()
        except OSError:
            continue
        if key in seen:
            continue
        seen.append(key)
        present = [parent / n for n in LIB_FILES if (parent / n).is_file()]
        if present:
            # Earlier candidates win a tie, so the root stays the default.
            layouts.append((len(present), len(seen), parent, present))
    if not layouts:
        return [], list(LIB_FILES), None
    count, order, parent, present = max(layouts, key=lambda l: (l[0], -l[1]))
    missing = [n for n in LIB_FILES if not (parent / n).is_file()]
    own = len([n for n in LIB_FILES if (candidates[0] / n).is_file()])
    note = None
    if parent != candidates[0] and own:
        note = ("reading the more complete set in %s (%d of %d binding sources), "
                "not the partial copy in %s (%d file)"
                % (parent, count, len(LIB_FILES), candidates[0], own))
    return present, missing, note
# --------------------------------------------------------------------------
# One function body
# --------------------------------------------------------------------------

class Slot:
    __slots__ = ("index", "reads", "absent", "variadic", "name")

    def __init__(self, index):
        self.index = index
        self.reads = []      # (lua_type, evidence)
        self.absent = []     # guards saying the argument may be left out
        self.variadic = []   # evidence that extra arguments are read here
        self.name = None

    def add(self, lua_type, evidence):
        if lua_type and (lua_type, evidence) not in self.reads:
            self.reads.append((lua_type, evidence))

    def type_expr(self, optional):
        typed = [t for t in self.reads if t[0] in TYPE_ORDER]
        unknown = [t for t in self.reads if t[0] not in TYPE_ORDER]
        if not typed:
            if unknown:
                return join_types(t[0] for t in unknown)
            return UNKNOWN
        # `nil` never replaces a real type: it only marks that the argument
        # may be omitted.  Several distinct real types mean the caller may pass
        # any of them (Group.Filter's 3rd argument is a Card, a Group or nil).
        real = [t[0] for t in typed if t[0] != "nil"]
        if not real:
            return "nil" if not optional else UNKNOWN
        names = sorted(set(real), key=type_key)
        if "nil" in [t[0] for t in typed] and "nil" not in names:
            names.insert(0, "nil")
        return join_types(names)
    def evidence(self):
        return sorted(set(e for _, e in self.reads))


def function_bodies(lib):
    """Yield (symbol, body_text, body_clean) for every scriptlib definition."""
    for m in DEF_START.finditer(lib.clean):
        start = lib.clean.index("{", m.end() - 1)
        end = match_pair(lib.clean, start, "{", "}")
        # Strip the outer braces: statements directly in the body are at depth 0,
        # which is what return detection needs.
        yield m.group(1), lib.raw[start + 1:end], lib.clean[start + 1:end]


def analyze_body(raw_body, clean_body, where, consts, callee_returns):
    """Infer required count, arguments and return values for one body.

    Only statements inside the body are used; every inferred fact keeps the
    statement it came from in ``evidence``.
    """
    body = mask_lambdas(clean_body)
    slots = {}
    issues = []
    notes = []

    def slot(i):
        if i not in slots:
            slots[i] = Slot(i)
        return slots[i]

    aliases = dict(consts)
    for m in SIMPLE_ASSIGN.finditer(body):
        value = int_value(m.group(3), aliases)
        if value is not None:
            aliases[m.group(2)] = value
    # `for(int32_t i = 2; i <= lua_gettop(L); ++i)` reads arguments starting
    # at 2, so the loop variable itself carries the tail's first index.
    loop_vars = {}
    for m in LOOP_DECL.finditer(body):
        start = int_value(m.group(2), aliases)
        loop_vars[m.group(1)] = start
    minimum, min_evidence = None, None
    m = re.search(r"check_param_count\s*\(\s*L\s*,\s*(\w+)\s*\)", body)
    if m:
        minimum = int_value(m.group(1), aliases)
        if minimum is None:
            issues.append("%s: check_param_count(L, %s) has an unknown value" % (where, m.group(1)))
            minimum = 0
        min_evidence = "check_param_count(L, %s)" % m.group(1)

    # `lua_gettop(L) - 3` is how the variadic tail is measured: arguments above
    # the fixed ones start at 4.
    vararg_base = None
    vararg_stmt = None
    for m in re.finditer(r"lua_gettop\s*\(\s*L\s*\)\s*-\s*(\w+)", body):
        fixed = int_value(m.group(1), aliases)
        if fixed is not None:
            vararg_base = fixed + 1
            vararg_stmt = statement_text(raw_body, m.end())
            notes.append("variadic tail measured as %s" % vararg_stmt)
            break

    for m in SLOT_READ.finditer(body):
        name = m.group(1)
        kind, value, args = slot_index(body, m, aliases, loop_vars)
        if kind is None:
            issues.append("%s: cannot resolve the stack index in `%s`"
                          % (where, statement_text(raw_body, m.end())))
            continue
        lua_type, nilable = None, False
        if name == "check_param":
            param_kind = args[1].strip() if len(args) > 1 else ""
            lua_type = PARAM_TYPES.get(param_kind)
            if lua_type is None:
                issues.append("%s: check_param(%s) has no Lua type" % (where, param_kind))
                continue
            # The fourth argument is documented as "accept nil as well".
            nilable = len(args) >= 4 and args[3].strip() == "TRUE"
        elif name in ("check_param_count", "lua_gettop", "lua_isnil", "lua_isnone",
                      "lua_isnoneornil", "lua_isinteger", "lua_isnumber", "lua_isuserdata"):
            if name in ("lua_isnone", "lua_isnoneornil"):
                lua_type = "nil"
            else:
                continue
        elif name == "check_filter":
            lua_type = "function"
        elif name == "get_operation_value":
            lua_type = "int"
        elif name == "interpreter::get_function_handle":
            lua_type = "function"
        else:
            lua_type = READ_TYPES.get(name)
            if lua_type is None:
                continue
        text = statement_text(raw_body, m.end())
        if kind == "vararg":
            base = value if value is not None else (minimum or 0) + 1
            vararg_base = vararg_base or base
            s = slot(base)
            s.variadic.append(text)
            s.add(lua_type, text)
            if nilable:
                s.add("nil", text)
            continue
        if kind == "relative":
            notes.append("reads the stack relative to the top in `%s`" % text)
            continue
        if value == 0:
            notes.append("reads the return area in `%s`" % text)
            continue
        slot(value).add(lua_type, text)
        if nilable:
            slot(value).add("nil", text)

    for m in USERDATA_CAST.finditer(body):
        kind, value, args = slot_index(body, m, aliases, loop_vars)
        ctype = m.group(1)
        if ctype not in CAST_TYPES or kind is None or kind == "relative":
            continue
        text = statement_text(raw_body, m.end())
        lua_type = CAST_TYPES[ctype]
        if kind == "vararg":
            base = value if value is not None else (minimum or 0) + 1
            vararg_base = vararg_base or base
            slot(base).add(lua_type, text)
            slot(base).variadic.append(text)
        elif value != 0:
            slot(value).add(lua_type, text)

    # Names: `card* pcard = *(card**) lua_touserdata(L, 1)` -> pcard.
    for m in re.finditer(r"(?m)^\s*([\w:]+)\s*(?:\*\s*)?(\w+)\s*=\s*[^;]*?"
                         r"(?:lua_to\w+|lua_touserdata|check_param|get_function_handle)"
                         r"\s*\(.*?\)[^;]*;", body):
        ctype, var = m.group(1), m.group(2)
        if ctype not in LOCAL_TYPES or var in aliases:
            continue
        inner = m.group(0)
        read = SLOT_READ.search(inner)
        if not read:
            continue
        kind, value, _ = slot_index(inner, read, aliases, loop_vars)
        if kind and value and kind != "relative" and value != 0:
            s = slot(value)
            if s.name is None:
                s.name = var

    # Names from a plain assignment to a local declared earlier.  The common
    # optional-parameter shape declares a default and then overwrites it from
    # the stack:
    #     int32_t cp = pcard->current.controler;
    #     if(lua_gettop(L) >= 2 && !lua_isnil(L, 2))
    #         cp = (int32_t)lua_tointeger(L, 2);
    # Only one identifier precedes the `=`, so this cannot match a declaration.
    for m in re.finditer(r"(?m)^\s*([A-Za-z_]\w*)\s*=(?!=)\s*[^;]*?"
                         r"(?:lua_to\w+|lua_touserdata|check_param"
                         r"|get_function_handle)\s*\(.*?\)[^;]*;", body):
        var = m.group(1)
        read = SLOT_READ.search(m.group(0))
        if not read:
            continue
        kind, value, _ = slot_index(m.group(0), read, aliases, loop_vars)
        if kind and value and kind != "relative" and value != 0:
            s = slot(value)
            if s.name is None:
                s.name = var

    highest = max(slots) if slots else 0
    if minimum is None:
        limit = (vararg_base - 1) if vararg_base else highest
        minimum = max(min(limit, highest), 0)
        # No `check_param_count` to quote, so the count was worked out from the
        # highest stack index the body reads.  Cite that read itself: it is
        # still a statement a reader can search for in the file.
        reads = slots[minimum].evidence() if minimum in slots else []
        min_evidence = reads[0] if reads else derived(
            "no check_param_count and no argument read: the body takes no"
            " argument")

    for i in range(minimum + 1, highest + 1):
        if i in slots and not slots[i].absent:
            slots[i].absent.append("position above the required count")

    for m in re.finditer(r"lua_gettop\s*\(\s*L\s*\)\s*(>=|>)\s*(\w+)", body):
        bound = int_value(m.group(2), aliases)
        if bound is None:
            continue
        if m.group(1) == ">":
            bound += 1
        # The guard is what makes the argument optional, so quote the guard as
        # the author wrote it.  A bare `lua_gettop(L) >= 2` cannot be searched
        # for in the file and hides the `!lua_isnil` half of the condition.
        guard = guard_statement(raw_body, m.start())
        for i in range(bound, highest + 1):
            if i in slots:
                slots[i].add("nil", guard)

    args = []
    top = max(highest, minimum)
    for i in range(1, top + 1):
        s = slots.get(i) or Slot(i)
        optional = i > minimum or bool(s.absent)
        args.append({
            "position": i,
            "type": s.type_expr(optional),
            "optional": optional,
            "variadic": False,
            "name": s.name,
            "evidence": s.evidence(),
        })

    # The variadic tail occupies one signature slot; reads above its first
    # index are further values of the same tail, not extra arguments.
    if vararg_base is not None and args:
        tail = next((a for a in args if a["position"] == vararg_base), None)
        if tail is None and vararg_base == len(args) + 1:
            # The tail exists (it is counted from lua_gettop) but the values
            # are consumed by a helper such as check_filter, so no lua_to*
            # read names their type.
            tail = {"position": vararg_base, "type": UNKNOWN, "optional": True,
                    "variadic": True, "name": None,
                    "evidence": [vararg_stmt] if vararg_stmt else
                                [derived("tail counted from lua_gettop(L)")]}
            args.append(tail)
        extra = [a for a in args if a["position"] > vararg_base] if tail else []
        if tail is not None:
            for a in extra:
                if a["type"] != UNKNOWN and (tail["type"] == UNKNOWN or
                                             a["type"] not in tail["type"]):
                    tail["type"] = join_types(tail["type"].split("|") + [a["type"]])
                if a["name"] and not tail["name"]:
                    tail["name"] = a["name"]
                tail["evidence"].extend(a["evidence"])
            args = [a for a in args if a["position"] <= vararg_base]
            tail["variadic"] = True
            tail["optional"] = True

    for a in args:
        if a["type"] == UNKNOWN:
            if a["variadic"]:
                # The tail is real (it is counted from lua_gettop) but a helper
                # such as check_filter consumes its values, so no lua_to* read
                # names their type.  `...` states that plainly.
                notes.append("variadic tail from position %d read by a helper"
                             % a["position"])
                continue
            issues.append("warning: %s: argument %d has no readable type"
                          % (where, a["position"]))

    kinds, evidence = [], []
    for m in PUSH_CALL.finditer(body):
        token = m.group(1)
        if token in CONVERSIONS:
            kinds.append(CONVERSIONS[token])
            evidence.append(token)
        elif token in PUSHES:
            kinds.append(PUSHES[token])
            evidence.append(token)
        elif token == "lua_createtable":
            kinds.append(UNKNOWN)
            evidence.append(token)
    for m in re.finditer(r"return\s+(\w+)\s*\(.*?\);", body):
        helper = m.group(1)
        known = callee_returns.get(helper)
        if known and known.get("return"):
            kinds.append(known["return"])
            # Quote the forwarding statement itself; the callee's fixed count
            # is an inference and is marked as one.
            evidence.append(statement_text(raw_body, m.start()))

    yields = bool(re.search(r"return\s+lua_yieldk?\s*\(", body))
    pushed = []
    inner = ""
    cont_loop = False
    # (value_or_None, expression, quoted statement)
    cont_return = None
    if yields:
        # Same offsets in both texts; a lambda body only survives in the
        # unmasked source, so search there.
        m = re.search(r"return\s+lua_yieldk?\s*\(", clean_body)
        if m:
            open_paren = clean_body.index("(", m.end() - 1)
            close = match_pair(clean_body, open_paren, "(", ")")
            lam = re.search(r"\[\s*\]\s*\(.*?\)\s*(?:->[^ {]*)?\s*\{",
                            clean_body[open_paren:close])
            if lam:
                start = open_paren + lam.end() - 1
                end = match_pair(clean_body, start, "{", "}")
                inner = clean_body[start + 1:end]
                for mm in PUSH_CALL.finditer(inner):
                    token = mm.group(1)
                    if token in CONVERSIONS:
                        pushed.append(CONVERSIONS[token])
                    elif token in PUSHES:
                        pushed.append(PUSHES[token])
                # A push inside a loop pushes once per iteration, so the
                # number of statements is not the number of values.
                cont_loop = bool(re.search(r"\b(?:for|while)\s*\(", inner))
                for pos in find_returns(inner):
                    mm = re.match(r"return\s+([^;]+);", inner[pos:])
                    if mm:
                        expr = mm.group(1).strip()
                        cont_return = (int_value(expr, aliases), expr,
                                       statement_text(raw_body, start + 1 + pos))

    # Every top-level `return` of the main body, kept with its text so an
    # evidence line can cite the branch that returns early.
    main_returns = []
    for pos in find_returns(body):
        m = re.match(r"return\s+([^;]+);", body[pos:])
        if not m:
            continue
        expr = m.group(1).strip()
        if expr.startswith(("lua_yield", "luaL_error")):
            # A yield switches to the continuation; an error call unwinds the
            # stack.  Neither is a shape the script receives.
            continue
        main_returns.append((int_value(expr, aliases), expr,
                             statement_text(raw_body, pos)))

    # Which locals were filled from a Lua stack slot, so a varying return count
    # can be attributed to the caller's arguments rather than to game state.
    arg_vars = {}
    for text in (body, inner):
        for m in re.finditer(r"(\w+)\s*=\s*[^;]*?"
                             r"(?:lua_to[^\W_]+|lua_touserdata"
                             r"|interpreter::get_function_handle)\s*\(\s*L\s*,\s*([^)]*)\)",
                             text):
            arg_vars.setdefault(m.group(1), " ".join(m.group(2).split()))

    # `uint32_t args = lua_gettop(L) - 1;` is the count of extra arguments the
    # caller passed.  The body then pushes one value per flag, so the return
    # count follows the arguments, not the game state.
    arg_count_vars = {}
    for m in re.finditer(r"(\w+)\s*=\s*lua_gettop\s*\(\s*L\s*\)\s*"
                         r"-\s*(\w+)\s*;", body):
        arg_count_vars[m.group(1)] = "lua_gettop(L) - %s" % m.group(2)

    def delegated_count(expr):
        """Value count of `return f(L, ...)` where f returns a fixed count.

        A bare call expression returns whatever the callee returns.  When the
        callee's own arity is fixed (its body ends in `return 1`), the caller
        has that fixed arity too; treating the call as a runtime value would
        turn every `return card_is_code(L);` into a bogus `bool...`.
        """
        m = re.fullmatch(r"(?:scriptlib::)?(\w+)\s*\(.*\)", expr, re.S)
        if not m:
            return None
        info = callee_returns.get(m.group(1))
        if not info:
            return None
        callee = m.group(1)
        return (callee, info.get("count"), info.get("return"))

    def count_source(expr):
        """Where a varying return count is read from: 'arguments' or 'state'."""
        names = [n for n in re.findall(r"(?<![.>])[A-Za-z_][\w]*", expr)
                 if n not in ("L", "int", "int32_t", "uint32_t", "size_t", "return")]
        for name in names:
            if name in arg_vars:
                return ("arguments",
                        "the count is `%s`, read from the Lua argument at index %s"
                        % (name, arg_vars[name]))
            if name in arg_count_vars:
                return ("arguments",
                        "the count is `%s`, the number of extra arguments"
                        " (`%s`)" % (name, arg_count_vars[name]))
        return ("state",
                "the count is `%s`, which the body reads from the game state,"
                " not from an argument" % expr)

    body_loop = bool(re.search(r"\b(?:for|while)\s*\(", body))
    arity = "fixed"
    arity_cause = None
    count = None

    if yields and pushed:
        return_types = pushed
        if cont_return and cont_return[0] is not None:
            count = cont_return[0]
            evidence.append(cont_return[2])
            evidence.append(derived("the continuation therefore returns %d value%s"
                                    % (count, "" if count == 1 else "s")))
        elif cont_return:
            arity = "input-dependent"
            arity_cause, why = count_source(cont_return[1])
            evidence.append(cont_return[2])
            evidence.append(derived(why))
        elif cont_loop or body_loop:
            arity = "input-dependent"
            arity_cause = "state"
            evidence.append(derived("values are pushed in a loop whose length"
                                    " is a runtime value, not a fixed count"))
        else:
            count = len(pushed)
            evidence.append(derived("the continuation pushes %d value%s"
                                    % (count, "" if count == 1 else "s")))
    else:
        return_types = kinds
        if yields:
            evidence.append(derived("yields without a visible push"))
        literals = [v for v, _, _ in main_returns if v is not None]
        dynamic = [(t, q) for v, t, q in main_returns if v is None]
        if dynamic:
            expr, quote = dynamic[0]
            callee = delegated_count(expr)
            if callee and callee[1] is not None and len(dynamic) == 1:
                # The body hands its whole result to a callee with a fixed
                # count, so this function has that count too.
                count = callee[1]
                evidence.append(quote)
                evidence.append(derived("%s returns %d value%s"
                                        % (callee[0], count,
                                           "" if count == 1 else "s")))
            elif callee and callee[1] is not None:
                # Several return sites agree only if every one of them
                # delegates the same way; keep the shape, mark the arity
                # varying when a literal site disagrees with it.
                all_fixed = all((delegated_count(t) or (None, None, None))[1] is not None
                                for t, _ in dynamic)
                if all_fixed:
                    counts = {(delegated_count(t) or (None, None, None))[1]
                              for t, _ in dynamic}
                    if len(counts) == 1:
                        count = counts.pop()
                        evidence.extend(q for _, q in dynamic)
                        evidence.append(derived("every return site delegates to a"
                                                " function returning %d value%s"
                                                % (count, "" if count == 1 else "s")))
                    else:
                        arity = "input-dependent"
                        arity_cause = "state"
                        evidence.append(derived("return sites delegate to"
                                                " functions with different fixed"
                                                " counts"))
                else:
                    arity = "input-dependent"
                    arity_cause, why = count_source(expr)
                    evidence.append(quote)
                    evidence.append(derived(why))
            else:
                arity = "input-dependent"
                arity_cause, why = count_source(expr)
                evidence.append(quote)
                evidence.append(derived(why))
        elif literals:
            count = max(literals)
            for v, _, q in main_returns:
                if v == count:
                    evidence.append(q)
                    break
        elif return_types:
            count = 1
        elif yields:
            # `return lua_yield(L, 0)` with no continuation values: the script
            # resumes with nothing.
            count = 0

    # `return 0` on an error branch beside a success path that returns values
    # is worth stating: a caller must handle both shapes.
    zero_sites = [t for v, t, _ in main_returns if v == 0]
    value_sites = [t for v, t, _ in main_returns if v not in (None, 0)]
    if yields and zero_sites and (value_sites or arity == "input-dependent"):
        notes.append("returns 0 values on an early return (`return %s;`) and"
                     " one value per result on success" % zero_sites[0])

    if return_types:
        real = [k for k in return_types if k != "nil"]
        if not real:
            ret = "nil"
        else:
            ret = ",".join(real) if count and count > 1 else join_types(real)
            if arity == "input-dependent":
                # A trailing `...` on the return type means "one or more values
                # of this shape, as many as the call produced".
                ret += "..."
    elif count == 0:
        ret = "nil"
    else:
        ret = UNKNOWN
        issues.append("warning: %s: return type is not inferable" % where)

    return {
        "required": minimum,
        "min_evidence": min_evidence,
        "args": args,
        "return": ret,
        "return_count": count,
        "return_arity": arity,
        "return_arity_cause": arity_cause,
        "return_evidence": sorted(set(evidence)),
        "yields": yields,
        "issues": issues,
        "notes": notes,
    }

# --------------------------------------------------------------------------
# Hand-written annotations
# --------------------------------------------------------------------------

BLOCK_HEAD = re.compile(r"^(\S+)\s+([A-Za-z_]\w*\.\w+)\s*\(")
CJK = re.compile(r"[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]")
DOTTED_CALL = re.compile(r"(?:Card|Group|Effect|Duel|Debug)\.\w+\(")


def decode_text(data):
    """Decode bytes trying the encodings these files are actually stored in."""
    for enc in ("utf-8-sig", "utf-8", "gb18030", "big5"):
        try:
            return data.decode(enc), enc
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", "replace"), "utf-8 (lossy)"


def read_annotations(path):
    """Read a `●type Name(args)` annotation file.

    Returns ``(blocks, encoding, warnings)`` where each block is a dict with
    ``key`` (``Name.Function``), ``head`` (the authored `●` line), ``prose``
    (the author's description lines) and ``dropped`` (stale signature lines the
    previous tool wrote next to the hand-written text).
    """
    data = Path(path).read_bytes()
    text, encoding = decode_text(data)
    warnings = []
    if "\u25cf" not in text:
        warnings.append("%s: no ● markers; not an annotation file?" % Path(path).name)
    blocks = []
    for chunk in re.split(r"(?m)^[\ufeff]*(?=\u25cf)", text):
        if not chunk.strip():
            continue
        # Keep each line's own indentation: the author's nesting is content.
        lines = [l.rstrip() for l in chunk.replace("\r\n", "\n").split("\n")]
        markers = [i for i, l in enumerate(lines) if l.lstrip().startswith("\u25cf")]
        if markers:
            first = markers[0]
            del lines[:first]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        head = lines[0].strip().lstrip("\u25cf").strip()
        m = BLOCK_HEAD.match(head)
        if not m:
            warnings.append("%s: ● line without a signature: %r"
                            % (Path(path).name, head[:40]))
            continue
        body, prose, dropped = lines[1:], [], []
        # The previous tool wrote a second, C++-derived signature directly
        # below every hand-written ● line.  It is recognisable by position
        # (always first), by content (a dotted Namespace.Function call) and by
        # absence of Chinese text; nothing else in these files looks like that.
        if body and not CJK.search(body[0]) and DOTTED_CALL.search(body[0]):
            dropped.append(body.pop(0).strip())
        for line in body:
            stripped = line.strip()
            if stripped:
                prose.append(stripped.lstrip("\u25cf").strip()
                             if stripped.startswith("\u25cf") else stripped)
        blocks.append({
            "key": m.group(2),
            "type": m.group(1),
            "head": head,
            "prose": prose,
            "dropped": dropped,
        })
    return blocks, encoding, warnings

def render_arg(a):
    """One argument: `type name`, `type name...`, `[type name]` if optional."""
    name = a.get("name")
    piece = "%s %s" % (a["type"], name) if name else a["type"]
    if a["variadic"]:
        # `int tcode...` already says "zero or more", so no brackets.
        # A tail whose values are consumed by a helper has no visible element
        # type; `...` says that without pretending to know it.
        return "..." if a["type"] == UNKNOWN else piece + "..."
    if a["optional"]:
        return "[%s]" % piece
    return piece


def render_generated(record):
    """The `●return Name(args)` line built only from source evidence."""
    args = ", ".join(render_arg(a) for a in record["args"])
    return "\u25cf%s %s(%s)" % (record["return"], record["name"], args)


def render_block(record, annotations, mark):
    """One documentation block: the ● line, then the description lines.

    When the function has a hand-written block, that block is emitted exactly
    as its author wrote it.  Otherwise the generated line is used and, with
    ``--mark``, is labelled so a reader can tell which text came from the
    source and which from a person.
    """
    ann = annotations.get(record["name"]) if annotations else None
    out = []
    if ann:
        out.append("\u25cf" + ann["head"])
        out.extend(ann["prose"])
    else:
        out.append(render_generated(record))
        if mark:
            out.append(" (generated from %s; no hand-written description)"
                       % record["file"])
    return out


def render_text(result, annotations, mark):
    lines = []
    for record in result["functions"]:
        lines.extend(render_block(record, annotations, mark))
    if annotations:
        used = set(r["name"] for r in result["functions"])
        # dicts keep insertion order, so these stay in the order the file has
        extra = [b for k, b in annotations.items() if k not in used]
        if extra:
            lines.append("")
            lines.append("# Hand-written entries with no matching binding in the sources:")
            for b in extra:
                lines.append("\u25cf" + b["head"])
                lines.extend(b["prose"])
    return "\n".join(lines) + "\n"


def to_json(result):
    return json.dumps(result, ensure_ascii=False, indent=1, sort_keys=False)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def collect_bodies(lib):
    """Map symbol -> (raw body, clean body) for every scriptlib definition."""
    bodies = {}
    for symbol, raw_body, clean_body in function_bodies(lib):
        bodies[symbol] = (raw_body, clean_body)
    return bodies


def helper_returns(libs):
    """Return types of the delegating helpers (`return helper(L, MEMBER)`)."""
    found = {}
    for lib in libs:
        for m in HELPER_DEF.finditer(lib.clean):
            symbol = m.group(1)
            start = lib.clean.index("{", m.end() - 1)
            end = match_pair(lib.clean, start, "{", "}")
            body = mask_lambdas(lib.clean[start:end + 1])
            kinds = [PUSHES[p.group(1)] for p in PUSH_CALL.finditer(body) if p.group(1) in PUSHES]
            real = [k for k in kinds if k != "nil"] or ["nil"]
            # A helper returns a fixed number of values: its own `return N`.
            # When the body has more than one such literal, the count is not
            # fixed and a caller's delegation must stay unresolved.
            literals = {int(n) for n in re.findall(r"return\s+([0-9]+)\s*;", body)}
            fixed = literals.pop() if len(literals) == 1 else None
            found[symbol] = {"return": join_types(real),
                             "count": fixed,
                             "file": lib.name,
                             "body": body}
    return found


def analyze_corpus(libs):
    """Analyze every registered function; returns records plus diagnostics."""
    bodies = {}
    for lib in libs:
        for symbol, raw_body, clean_body in function_bodies(lib):
            bodies[(lib.name, symbol)] = (raw_body, clean_body)

    helpers = helper_returns(libs)
    # A body like `return card_is_code(L);` returns exactly what the callee
    # returns.  Only a callee whose own returns are a single literal `return N`
    # has a count this tool may propagate; anything else stays unresolved.
    callees = dict(helpers)
    for (fname, symbol), (raw_body, clean_body) in bodies.items():
        body = mask_lambdas(clean_body)
        values = []
        for pos in find_returns(body):
            m = re.match(r"return\s+([^;]+);", body[pos:])
            if m:
                values.append(m.group(1).strip())
        literals = {int(v) for v in values if re.fullmatch(r"[0-9]+", v)}
        if len(literals) == 1:
            kinds = [PUSHES[p.group(1)] for p in PUSH_CALL.finditer(body)
                     if p.group(1) in PUSHES]
            real = [k for k in kinds if k != "nil"]
            callees.setdefault(symbol, {"count": literals.pop(),
                                        "return": join_types(real) if real else None})
    records, issues = [], []
    for lib in libs:
        issues.extend(lib.issues)

    # Function bodies that only forward to another registered function return
    # whatever that function returns; resolve those by iteration.
    pending = {}
    by_symbol = {}
    for lib in libs:
        for lua, symbol, table, index in lib.entries:
            key = (lib.name, symbol)
            if key not in bodies:
                issues.append("%s: %r is registered to %s, which has no definition"
                              % (lib.name, lua, symbol))
                continue
            raw_body, clean_body = bodies[key]
            info = analyze_body(raw_body, clean_body, "%s:%s" % (lib.name, symbol),
                                lib.consts, callees)
            pending[(lib.name, lua)] = (lib, symbol, table, index, info, raw_body)
            by_symbol[(lib.name, symbol)] = (lib, symbol, table, index, info)

    for _ in range(4):
        changed = False
        for key, (lib, symbol, table, index, info, raw_body) in pending.items():
            if info["return"] != UNKNOWN or "is not inferable" not in " ".join(info["issues"]):
                continue
            m = re.search(r"return\s+(\w+)\s*\(", mask_lambdas(raw_body))
            if not m:
                continue
            other = by_symbol.get((lib.name, m.group(1)))
            if other and other[4]["return"] != UNKNOWN:
                info["return"] = other[4]["return"]
                info["return_count"] = other[4]["return_count"]
                info["return_arity"] = other[4]["return_arity"]
                info["return_arity_cause"] = other[4]["return_arity_cause"]
                info["return_evidence"] = [statement_text(raw_body, m.start()),
                                            derived("delegates to %s(...)"
                                                    % m.group(1))]
                info["issues"] = [i for i in info["issues"] if "not inferable" not in i]
                changed = True
        if not changed:
            break

    order = []
    for position, lib in enumerate(libs):
        for lua, symbol, table, index in lib.entries:
            order.append((position, index, lua, symbol, table))
    for position, index, lua, symbol, table in sorted(order):
        key = (libs[position].name, lua)
        entry = pending.get(key)
        if entry is None:
            continue
        lib, symbol, table_name, table_index, info, raw_body = entry
        records.append({
            "name": "%s.%s" % (lib.namespace, lua),
            "lua_name": lua,
            "namespace": lib.namespace,
            "symbol": symbol,
            "table": table_name,
            "table_index": table_index,
            "file": lib.name,
            "required": info["required"],
            "min_evidence": info["min_evidence"],
            "args": info["args"],
            "return": ("~" + info["return"]) if info["yields"] and info["return"] != UNKNOWN else info["return"],
            "return_count": info["return_count"],
            "return_arity": info["return_arity"],
            "return_arity_cause": info["return_arity_cause"],
            "return_evidence": info["return_evidence"],
            "yields": info["yields"],
            "issues": info["issues"],
            "notes": info["notes"],
        })
        issues.extend(info["issues"])

    names = [r["name"] for r in records]
    seen = {}
    for r in records:
        if r["name"] in seen:
            issues.append("%s: two registrations produce the same Lua name (%s and %s)"
                          % (r["name"], seen[r["name"]], r["symbol"]))
        seen[r["name"]] = r["symbol"]
    return {
        "tool": {"name": "ygoDocGen", "version": VERSION},
        "functions": records,
        "sources": [{"file": lib.name, "namespace": lib.namespace,
                     "namespace_evidence": lib.ns_evidence, "registrations": len(lib.entries)}
                    for lib in libs],
        "counts": {"functions": len(records), "issues": len(issues),
                   "yielding": sum(1 for r in records if r["yields"]),
                   "varying_arity": sum(1 for r in records if r["return_arity"] == "input-dependent"),
                   # Fields the tool honestly could not infer.  A variadic tail
                   # read by a helper is not counted: it is documented as `...`.
                   "unknown_types": sum(
                       1 for r in records
                       if r["return"].lstrip("~") == UNKNOWN
                       or any(a["type"] == UNKNOWN and not a["variadic"]
                              for a in r["args"]))},
        "issues": issues,
    }


def setup_stdio():
    """Make the document printable under whatever text encoding we were given.

    Windows hands a redirected script the console code page (cp1252, cp936,
    ...).  cp936 carries ``●`` and needs no help; cp1252 does not, and writing
    the first entry would abort the run with a UnicodeEncodeError after the
    JSON file had already been written.  So: keep the text writer whenever it
    can represent the document, otherwise write UTF-8 bytes, and let stderr
    degrade escapes rather than raise.

    Returns True when the caller must write ``document.encode("utf-8")`` to
    ``sys.stdout.buffer`` instead of using ``sys.stdout.write``.
    """
    enc = getattr(sys.stdout, "encoding", None)
    if not enc:
        return False                      # StringIO in tests, real pipes on POSIX
    try:
        MARKER.encode(enc)
    except (UnicodeError, LookupError):
        pass
    else:
        return False                     # cp936, utf-8, ...: nothing to change

    err = getattr(sys.stderr, "errors", None)
    if err not in ("backslashreplace", "replace", "ignore"):
        try:
            sys.stderr.reconfigure(errors="backslashreplace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass

    stream = getattr(sys.stdout, "buffer", None)
    if stream is None:
        print("ygoDocGen: stdout encoding %s cannot represent %r; writing UTF-8"
              % (enc, MARKER), file=sys.stderr)
        return False
    print("ygoDocGen: stdout encoding %s cannot represent %r; writing UTF-8 bytes "
          "(run python -X utf8 or set PYTHONIOENCODING=utf-8 for a readable console)"
          % (enc, MARKER), file=sys.stderr)
    return True


def write_atomic(path, text):
    """Write ``text`` to ``path`` only when the whole payload is ready.

    The previous file stays untouched if anything fails, so a rerun that
    errors cannot leave a truncated JSON or document behind.
    """
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(prefix=Path(path).name + ".", suffix=".tmp",
                                   dir=str(Path(path).parent or "."))
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
        return True
    except OSError as exc:
        print("ygoDocGen: error: could not write %s: %s" % (path, exc), file=sys.stderr)
        print("  the previous file is still intact", file=sys.stderr)
        if tmp and os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ygoDocGen.py",
        description="Generate YGOPro Lua API documentation from ocgcore binding sources.")
    parser.add_argument("--dir", default=".",
                        help="directory holding libcard.cpp and friends (default: .)")
    parser.add_argument("--annotations", metavar="FILE",
                        help="merge hand-written entry blocks (U+25CF marker) from this file")
    parser.add_argument("--json", metavar="FILE",
                        help="write full records, including evidence, to FILE")
    parser.add_argument("--check", action="store_true",
                        help="report defects and exit non-zero instead of printing")
    parser.add_argument("--mark", action="store_true",
                        help="mark entries that had no hand-written annotation")
    parser.add_argument("--strict", action="store_true",
                        help="with --check only: also exit non-zero on inferred unknowns")
    args = parser.parse_args(argv)

    # Before anything is printed: a console code page without `●` would fail
    # mid-run (possibly after the JSON file was written).  Nothing has been
    # written yet, so a failure here cancels the whole run cleanly.
    try:
        binary_stdout = setup_stdio()
    except Exception as exc:                      # noqa: BLE001 - report, do not traceback
        print("ygoDocGen: error: cannot write to stdout in this console encoding: %s"
              % exc, file=sys.stderr)
        print("  no file was written; the previous document is still intact",
              file=sys.stderr)
        return 1

    if args.strict and not args.check:
        # `--strict` only qualifies a check; on its own it would look like it
        # had verified something while printing a document.
        print("ygoDocGen: error: --strict only modifies --check", file=sys.stderr)
        print("  use: ygoDocGen.py --check --strict [--dir DIR]", file=sys.stderr)
        return 2
    if args.check:
        return check(args)

    root = Path(args.dir)
    libs, missing, layout = find_libs(root)
    if not libs:
        print("ygoDocGen: no binding sources found under %s" % root, file=sys.stderr)
        print("  looked for: %s" % ", ".join(LIB_FILES), file=sys.stderr)
        return 2
    if layout:
        print("ygoDocGen: %s" % layout, file=sys.stderr)
    if missing:
        print("ygoDocGen: warning: incomplete sources under %s; missing %s"
              % (root, ", ".join(missing)), file=sys.stderr)
        print("  the document below covers only the bindings that are present",
              file=sys.stderr)

    result = analyze_corpus([Lib(p) for p in libs])
    result["missing_sources"] = missing
    annotations = {}
    if args.annotations:
        blocks, encoding, warnings = read_annotations(args.annotations)
        annotations = {b["key"]: b for b in blocks}
        for warning in warnings:
            print("ygoDocGen: %s" % warning, file=sys.stderr)
        print("ygoDocGen: %d annotation blocks from %s (%s)"
              % (len(blocks), args.annotations, encoding), file=sys.stderr)

    # Both outputs are built completely before either file is touched: a bug
    # in one renderer must not destroy the other file from a previous run.
    try:
        document = render_text(result, annotations, args.mark)
        payload = to_json(result) + "\n" if args.json else None
        # Encode here, while a failure can still cancel the whole run, so the
        # write below cannot die after the JSON file is already on disk.
        document_bytes = document.encode("utf-8") if binary_stdout else None
    except Exception as exc:                      # noqa: BLE001 - report, do not traceback
        print("ygoDocGen: error: could not build the document: %s: %s"
              % (type(exc).__name__, exc), file=sys.stderr)
        print("  no file was written; the previous document is still intact",
              file=sys.stderr)
        return 1

    if args.json:
        if not write_atomic(args.json, payload):
            return 1
        print("ygoDocGen: wrote %s" % args.json, file=sys.stderr)

    if binary_stdout:
        sys.stdout.buffer.write(document_bytes)
        sys.stdout.buffer.flush()
    else:
        sys.stdout.write(document)
    return 0


def check(args):
    """Verify the sources.  Exit 2 on missing input, 1 on a structural defect.

    A *defect* is a claim the registry and the C++ bodies disagree about (a
    registration with no definition, a duplicate Lua name, a symbol whose
    prefix contradicts its namespace) or an input file the tool was told to
    document but did not find.  A *warning* is a field the tool honestly could
    not infer and printed as `?`; the document is still complete.  ``--strict``
    promotes warnings to failures for callers that require full type coverage.
    """
    libs, missing, layout = find_libs(Path(args.dir))
    if not libs:
        print("ygoDocGen: no binding sources found under %s" % args.dir, file=sys.stderr)
        return 2
    if layout:
        print("%s" % layout)
    result = analyze_corpus([Lib(p) for p in libs])
    counts = result["counts"]
    defects = [i for i in result["issues"] if not i.startswith("warning: ")]
    warnings = [i[len("warning: "):] for i in result["issues"] if i.startswith("warning: ")]
    for name in missing:
        defects.append("missing source file: %s (partial checkout)" % name)
    print("functions: %d" % counts["functions"])
    for source in result["sources"]:
        print("  %-14s %-7s %4d registrations"
              % (source["file"], source["namespace"], source["registrations"]))
    for name in missing:
        print("  %-14s %-7s    0 registrations (MISSING)" % (name, "?"))
    print("yielding: %d   unknown fields: %d   defects: %d   warnings: %d"
          % (counts["yielding"], counts["unknown_types"], len(defects), len(warnings)))
    if defects:
        print("\ndefects:")
        for issue in defects:
            print("  " + issue)
    if warnings:
        print("\nwarnings (inferred as ?):")
        for issue in warnings:
            print("  " + issue)
        if not args.strict:
            print("\n(inferred unknowns do not fail the check; use --strict to require them)")
    if defects or (args.strict and warnings):
        return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())
