"""Acceptance tests for ygoDocGen.py.

Every test here answers a question a user of the tool would ask:

* do the documented names come from the registration table, not the C symbol?
* are optional, variadic and coroutine-arity arguments described honestly?
* does merging hand-written annotations keep the author's text and drop the
  stale machine-written signature the old tool left behind?
* can a failing run destroy the document from a previous good run?
* is the output byte-identical across hash seeds?
* do the ``--check`` exit codes mean what the README says?

The synthetic fixture is small on purpose: it is a copy of the shapes the real
ocgcore sources use, with the expected answer written by hand next to it.  The
real-corpus tests run when a checkout is available and are skipped otherwise.
They look for one via ``YGODOCGEN_CORPUS`` first, then beside this repository
(``ocgcore/``, ``src/``, ``ygopro-core/``, ``ygopro-core/ocgcore/``, a sibling
``ocgcore`` directory), so a clean copy works with no configuration.
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def find_corpus():
    """Where the real ocgcore sources are, or None to skip those tests.

    ``YGODOCGEN_CORPUS`` wins when set (an empty value forces skip); otherwise
    the usual layouts next to this repo are tried, so no local path has to be
    hard-coded for the suite to cover the real corpus.
    """
    env = os.environ.get("YGODOCGEN_CORPUS")
    if env is not None:
        return Path(env)
    here = ROOT.parent
    for candidate in [ROOT, here / "ocgcore", here / "src",
                      here / "ygopro-core", here / "ygopro-core" / "ocgcore"]:
        if (candidate / "libcard.cpp").is_file():
            return candidate
    return None


CORPUS = find_corpus()

# The counts in the README are frozen at one upstream commit.  Checking out a
# different revision must not fail the suite: the invariants below are what
# actually has to hold, the numbers are only what that revision happened to
# contain.  The fingerprint is over the five binding sources, so a plain copy
# of the checkout (no .git) is recognised too.
PINNED_COMMIT = "2e47dbead97c3826d2f0779ed3ccb78fde772866"
PINNED_FINGERPRINT = "fca9483b023bb30eaf66ebf77da02d03afedafffded71154f7eeb6e9614f2100"
PINNED_COUNTS = {"Card": 276, "Duel": 229, "Effect": 55, "Group": 40, "Debug": 11}
PINNED_TOTAL = sum(PINNED_COUNTS.values())

import ygoDocGen  # noqa: E402


LIBCARD = """\
#include "scriptlib.h"

int32_t scriptlib::card_get_original_code(lua_State *L) {
\tcheck_param_count(L, 1);
\tcard* pcard = *(card**)lua_touserdata(L, 1);
\tif(pcard == nullptr) {
\t\tlua_pushnil(L);
\t\treturn 1;
\t}
\tlua_pushinteger(L, pcard->data.code);
\treturn 1;
}

int32_t scriptlib::card_is_set_card(lua_State *L) {
\tcheck_param_count(L, 1);
\tcard* pcard = *(card**)lua_touserdata(L, 1);
\tlua_pushboolean(L, pcard->data.type & TYPE_SET);
\treturn 1;
}

static const struct luaL_Reg cardlib[] = {
\t{ "GetOriginalCode", scriptlib::card_get_original_code },
\t{ "IsSetCard", scriptlib::card_is_set_card },
\t{ NULL, NULL }
};

void scriptlib::open_cardlib(lua_State *L) {
\tluaL_newlib(L, cardlib);
\tlua_setglobal(L, "Card");
}
"""

LIBDUEL = """\
#include "scriptlib.h"

int32_t scriptlib::duel_get_player_count(lua_State *L) {
\tcheck_param_count(L, 1);
\tint32_t playerid = (int32_t)lua_tointeger(L, 1);
\tint32_t mode = 0;
\tif(lua_gettop(L) >= 2 && !lua_isnil(L, 2))
\t\tmode = (int32_t)lua_tointeger(L, 2);
\tlua_pushinteger(L, mode + playerid);
\treturn 1;
}

int32_t scriptlib::duel_get_zone_cards(lua_State *L) {
\tcheck_param_count(L, 2);
\tint32_t playerid = (int32_t)lua_tointeger(L, 1);
\tint32_t location = (int32_t)lua_tointeger(L, 2);
\tfor(int32_t i = 3; i <= lua_gettop(L); ++i)
\t\tlua_tointeger(L, i);
\tlua_pushinteger(L, playerid + location);
\treturn 1;
}

int32_t scriptlib::duel_announce_number(lua_State *L) {
\tcheck_param_count(L, 2);
\tint32_t playerid = (int32_t)lua_tointeger(L, 1);
\t/* The real body collects every option from argument 2 upward, so the
\t   variadic tail is the documented shape there too. */
\tfor(int32_t i = 2; i <= lua_gettop(L); ++i)
\t\t(void)lua_tointeger(L, i);
\treturn lua_yieldk(L, 0, (lua_KContext)playerid, [](lua_State *L, int32_t status, lua_KContext ctx) {
\t\tlua_pushinteger(L, 1);
\t\tlua_pushinteger(L, 2);
\t\treturn 2;
\t});
}

int32_t scriptlib::duel_toss_coin(lua_State *L) {
\tcheck_param_count(L, 2);
\tint32_t playerid = (int32_t)lua_tointeger(L, 1);
\tint32_t count = (int32_t)lua_tointeger(L, 2);
\tif(count < 1)
\t\treturn 0;
\treturn lua_yieldk(L, 0, (lua_KContext)playerid, [](lua_State *L, int32_t status, lua_KContext ctx) {
\t\tint32_t n = (int32_t)lua_tointeger(L, 2);
\t\tfor(int32_t i = 0; i < n; ++i)
\t\t\tlua_pushinteger(L, i);
\t\treturn n;
\t});
}

static const struct luaL_Reg duellib[] = {
\t{ "GetPlayerCount", scriptlib::duel_get_player_count },
\t{ "GetZoneCards", scriptlib::duel_get_zone_cards },
\t{ "AnnounceNumber", scriptlib::duel_announce_number },
\t{ "TossCoin", scriptlib::duel_toss_coin },
\t{ NULL, NULL }
};

void scriptlib::open_duellib(lua_State *L) {
\tluaL_newlib(L, duellib);
\tlua_setglobal(L, "Duel");
}
"""

# A registration whose C++ body does not exist: the one structural defect the
# check must fail on.
LIBDEBUG_BROKEN = """\
#include "scriptlib.h"

int32_t scriptlib::debug_message(lua_State *L) {
\tcheck_param_count(L, 1);
\tlua_pushnil(L);
\treturn 1;
}

static const struct luaL_Reg debuglib[] = {
\t{ "Message", scriptlib::debug_message },
\t{ "ShowHint", scriptlib::debug_show_hint },
\t{ NULL, NULL }
};

void scriptlib::open_debuglib(lua_State *L) {
\tluaL_newlib(L, debuglib);
\tlua_setglobal(L, "Debug");
}
"""

# One argument the body never reads, plus one that is only guarded by a nil
# check: both are honest `?` warnings.
LIBSTRICT = """\
#include "scriptlib.h"

int32_t scriptlib::duel_is_chain_negatable(lua_State *L) {
\tcheck_param_count(L, 1);
\tlua_pushboolean(L, 1);
\treturn 1;
}

int32_t scriptlib::duel_is_chain_negatable2(lua_State *L) {
\tcheck_param_count(L, 1);
\tlua_pushboolean(L, 1);
\treturn 1;
}

static const struct luaL_Reg duellib[] = {
\t{ "IsChainNegatable", scriptlib::duel_is_chain_negatable },
\t{ "IsChainNegatable2", scriptlib::duel_is_chain_negatable2 },
\t{ NULL, NULL }
};

void scriptlib::open_duellib(lua_State *L) {
\tluaL_newlib(L, duellib);
\tlua_setglobal(L, "Duel");
}
"""

# The other three libraries exist in every real checkout.  The tool reports
# a missing lib file as a defect, and a lib file that declares no
# registration as one too, so a complete fixture needs both the file and one
# real entry in it.  Each stub documents `Noop` in its own namespace.
LIBSTUB = """\
#include "scriptlib.h"

int32_t scriptlib::%(symbol)s(lua_State *L) {
\tcheck_param_count(L, 0);
\tlua_pushnil(L);
\treturn 1;
}

static const struct luaL_Reg %(table)s[] = {
\t{ "Noop", scriptlib::%(symbol)s },
\t{ NULL, NULL }
};

void scriptlib::open_%(table)s(lua_State *L) {
\tluaL_newlib(L, %(table)s);
\tlua_setglobal(L, "%(ns)s");
}
"""

ANNOTATIONS = """\
●int Card.GetOriginalCode(card pcard)
int Card.GetOriginCode(card pcard)
返回c的卡片记载的代号
●void aux.ExtraOnly(Card c)
只存在于手写文档里的条目
"""


def write_libs(directory, files):
    for name, text in files.items():
        (directory / name).write_text(text, encoding="utf-8")


def corpus_commit(root):
    """The git revision of *root*, or None when it is not a checkout."""
    try:
        proc = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def corpus_fingerprint(root):
    """sha256 over the binding sources, in a fixed order ('' if incomplete)."""
    import hashlib
    digest = hashlib.sha256()
    for name in ygoDocGen.LIB_FILES:
        path = Path(root) / name
        if not path.is_file():
            return ""
        hexdigest = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(name.encode())
        digest.update(hexdigest.encode())
    return digest.hexdigest()


def is_pinned(root):
    """True when *root* is the revision this README's numbers were measured on.

    A checkout of another revision must not make the suite fail: the tool is
    supposed to be pointed at newer sources, and the counts in the README are
    one revision's facts.  What holds at every revision is checked separately.
    """
    return (corpus_fingerprint(root) == PINNED_FINGERPRINT
            or corpus_commit(root) == PINNED_COMMIT)


def run(argv):
    """Run the CLI in-process; returns (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = ygoDocGen.main(argv)
    return code, out.getvalue(), err.getvalue()


class Fixture(unittest.TestCase):
    """Shared synthetic checkout: Card, Duel and a broken Debug library."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        write_libs(self.dir, {"libcard.cpp": LIBCARD, "libduel.cpp": LIBDUEL})
        self.add_stubs()

    def add_stubs(self):
        for table, ns, symbol in (("effectlib", "Effect", "effect_noop"),
                                  ("grouplib", "Group", "group_noop"),
                                  ("debuglib", "Debug", "debug_noop")):
            name = "lib%s.cpp" % table[:-3]
            (self.dir / name).write_text(
                LIBSTUB % {"table": table, "ns": ns, "symbol": symbol},
                encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def doc(self, *extra):
        code, out, err = run(["--dir", str(self.dir)] + list(extra))
        self.assertEqual(code, 0, err)
        return out


class TestNames(Fixture):
    def test_lua_name_comes_from_the_registration_table(self):
        """The C symbol `card_get_original_code` is not the name a script types."""
        out = self.doc()
        self.assertIn("Card.GetOriginalCode(", out)
        self.assertNotIn("GetOriginCode(", out)
        self.assertNotIn("GetOriginalCode\"", out)

    def test_namespaces_come_from_lua_setglobal(self):
        code = self.doc("--json", str(self.dir / "out.json"))
        data = json.loads((self.dir / "out.json").read_text(encoding="utf-8"))
        namespaces = {s["file"]: s["namespace"] for s in data["sources"]}
        self.assertEqual(namespaces["libcard.cpp"], "Card")
        self.assertEqual(namespaces["libduel.cpp"], "Duel")
        for source in data["sources"]:
            self.assertIn("open_", source["namespace_evidence"])

    def test_every_record_carries_its_symbol_and_file(self):
        out = self.doc("--json", str(self.dir / "out.json"))
        data = json.loads((self.dir / "out.json").read_text(encoding="utf-8"))
        for record in data["functions"]:
            self.assertTrue(record["symbol"].startswith(record["namespace"].lower() + "_"))
            self.assertEqual(record["name"],
                             "%s.%s" % (record["namespace"], record["lua_name"]))
            self.assertTrue(record["file"].endswith(".cpp"))


class TestArguments(Fixture):
    def test_optional_argument_is_bracketed(self):
        # The guard is `lua_gettop(L) >= 2 && !lua_isnil(L, 2)`, so the caller
        # may pass an int or nothing: the brackets and the `nil` both say so.
        out = self.doc()
        self.assertIn("Duel.GetPlayerCount(int playerid, [nil|int mode])", out)

    def test_variadic_tail_is_rendered_with_ellipsis(self):
        # `for(i = 3; i <= lua_gettop(L); ++i) lua_tointeger(L, i)` reads a
        # loop-relative index, so the tail may be empty or any length.
        out = self.doc()
        self.assertIn("Duel.GetZoneCards(int playerid, int location, int...)", out)
        self.assertNotIn("Duel.GetZoneCards(?, ?", out)

    def test_argument_evidence_names_the_read(self):
        self.doc("--json", str(self.dir / "out.json"))
        data = json.loads((self.dir / "out.json").read_text(encoding="utf-8"))
        record = next(r for r in data["functions"] if r["name"] == "Card.GetOriginalCode")
        self.assertEqual(record["args"][0]["type"], "card")
        self.assertTrue(any("lua_touserdata" in e for e in record["args"][0]["evidence"]))
        self.assertEqual(record["min_evidence"], "check_param_count(L, 1)")


class TestReturnArity(Fixture):
    def test_fixed_multi_return_from_continuation(self):
        out = self.doc()
        self.assertIn("\u25cf~int,int Duel.AnnounceNumber(int playerid, int...)", out)

    def test_arity_that_depends_on_an_argument_is_not_reported_as_fixed(self):
        "\u25cf~int... Duel.TossCoin(int playerid, int count)"
        out = self.doc()
        self.assertIn("\u25cf~int... Duel.TossCoin(", out)
        self.assertNotIn("\u25cf~int Duel.TossCoin(", out)
        self.doc("--json", str(self.dir / "out.json"))
        data = json.loads((self.dir / "out.json").read_text(encoding="utf-8"))
        toss = next(r for r in data["functions"] if r["name"] == "Duel.TossCoin")
        self.assertEqual(toss["return_arity"], "input-dependent")
        self.assertIsNone(toss["return_count"])
        self.assertEqual(toss["return_arity_cause"], "arguments")
        self.assertTrue(any("read from the Lua argument at index 2"
                            in e for e in toss["return_evidence"]))
        # The early `return 0` must be stated, not averaged away.
        self.assertTrue(any("early return" in note for note in toss["notes"]))

    def test_yield_without_pushed_values_is_nil(self):
        """`return lua_yield(L, 0)` with nothing pushed resumes with no values."""
        lib = """\
#include "scriptlib.h"

int32_t scriptlib::duel_announce_coin(lua_State *L) {
\tcheck_param_count(L, 2);
\tint32_t playerid = (int32_t)lua_tointeger(L, 1);
\tint32_t count = (int32_t)lua_tointeger(L, 2);
\tif(count == 0)
\t\treturn 0;
\treturn lua_yieldk(L, 0, (lua_KContext)playerid, [](lua_State *L, int32_t status, lua_KContext ctx) {
\t\treturn 0;
\t});
}

static const struct luaL_Reg duellib[] = {
\t{ "AnnounceCoin", scriptlib::duel_announce_coin },
\t{ NULL, NULL }
};

void scriptlib::open_duellib(lua_State *L) {
\tluaL_newlib(L, duellib);
\tlua_setglobal(L, "Duel");
}
"""
        (self.dir / "libduel.cpp").write_text(lib, encoding="utf-8")
        self.doc("--json", str(self.dir / "out.json"))
        data = json.loads((self.dir / "out.json").read_text(encoding="utf-8"))
        rec = next(r for r in data["functions"] if r["name"] == "Duel.AnnounceCoin")
        self.assertEqual(rec["return"], "~nil")
        self.assertEqual(rec["return_count"], 0)
        self.assertTrue(rec["yields"])
        self.assertEqual(rec["return_arity"], "fixed")


class TestAnnotations(Fixture):
    def prepare(self, encoding="gb18030", text=ANNOTATIONS):
        path = self.dir / "functions.txt"
        path.write_bytes(text.encode(encoding))
        return path

    def test_author_text_wins_and_stale_signature_is_dropped(self):
        path = self.prepare()
        out = self.doc("--annotations", str(path), "--json", str(self.dir / "out.json"))
        self.assertIn("\u25cfint Card.GetOriginalCode(card pcard)", out)
        self.assertIn("返回c的卡片记载的代号", out)
        # The machine-written second signature the old tool left behind is
        # recognisable (dotted call, no Chinese) and must not survive.
        self.assertNotIn("Card.GetOriginCode", out)

    def test_utf8_bom_annotations_decode_too(self):
        path = self.prepare(encoding="utf-8-sig")
        out = self.doc("--annotations", str(path))
        self.assertIn("返回c的卡片记载的代号", out)
        self.assertNotIn("\ufeff", out)

    def test_hand_written_only_entries_are_kept_at_the_end(self):
        out = self.doc("--annotations", str(self.prepare()))
        tail = out.split("no matching binding")[-1]
        self.assertIn("aux.ExtraOnly", tail)
        self.assertIn("只存在于手写文档里的条目", tail)

    def test_generated_only_entries_are_marked_on_request(self):
        out = self.doc("--annotations", str(self.prepare()), "--mark")
        self.assertIn("(generated from libduel.cpp; no hand-written description)", out)


class TestEvidenceProvenance(Fixture):
    """`--json` evidence must be a quote or say that it is not one.

    A reader checks a field by searching the named file for the quoted
    statement.  If the tool paraphrases without saying so, that check silently
    fails and the evidence stops being evidence.  So every string is either
    verbatim (whitespace aside) in the file the record names, or begins with
    `derived: `.
    """

    def records(self):
        self.doc("--json", str(self.dir / "out.json"))
        data = json.loads((self.dir / "out.json").read_text(encoding="utf-8"))
        sources = {}
        for name in ("libcard.cpp", "libduel.cpp", "libeffect.cpp",
                     "libgroup.cpp", "libdebug.cpp"):
            if (self.dir / name).is_file():
                sources[name] = " ".join(
                    (self.dir / name).read_text(encoding="utf-8").split())
        return data["functions"], sources

    def test_every_evidence_string_is_a_quote_or_marked_derived(self):
        records, sources = self.records()
        checked = 0
        for record in records:
            quoted = ([record["min_evidence"]] + record["return_evidence"]
                      + [e for a in record["args"] for e in a["evidence"]])
            for text in quoted:
                self.assertTrue(text, record["name"] + " has an empty evidence string")
                if text.startswith(ygoDocGen.DERIVED):
                    continue
                checked += 1
                self.assertIn(" ".join(text.split()), sources[record["file"]],
                              "%s cites %r, which is not a statement in %s"
                              % (record["name"], text, record["file"]))
        self.assertGreater(checked, 10, "the fixture must quote real statements")

    def test_evidence_is_a_whole_statement(self):
        """A quote is a statement or a whole `if(...)` condition, never a slice.

        The two shapes evidence legitimately has are a statement ending in `;`
        and the header of a guard, `if(...)`, which is quoted in full so that
        both halves of the condition survive.
        """
        records, sources = self.records()
        for record in records:
            for arg in record["args"]:
                for text in arg["evidence"]:
                    if text.startswith(ygoDocGen.DERIVED):
                        continue
                    self.assertEqual(text.count("("), text.count(")"),
                                     "%s quotes an unbalanced fragment: %r"
                                     % (record["name"], text))
                    self.assertTrue(
                        text.startswith(("if(", "if (", "while(", "else if"))
                        or text.endswith((";", "{")) or "(" not in text,
                        "%s quotes a fragment that stops early: %r"
                        % (record["name"], text))

    def test_arguments_evidence_names_the_read_that_set_it(self):
        """The optional argument cites the guard, not just the assignment."""
        records, _ = self.records()
        duel = next(r for r in records if r["name"] == "Duel.GetPlayerCount")
        second = duel["args"][1]
        self.assertTrue(second["optional"])
        # Both halves of the guard matter: the bound and the nil check.
        self.assertIn("if(lua_gettop(L) >= 2 && !lua_isnil(L, 2))",
                      second["evidence"])
        self.assertIn("mode = (int32_t)lua_tointeger(L, 2);", second["evidence"])

    def test_the_record_has_no_duplicate_note_list(self):
        """`notes` is the one list; a mirrored `remarks` would only be a copy."""
        records, _ = self.records()
        for record in records:
            self.assertNotIn("remarks", record)


class TestOutputSafety(Fixture):
    def test_failure_never_clobbers_a_previous_document(self):
        """The supervisor's repro: JSON written, then the text renderer crashed."""
        target = self.dir / "docs.json"
        target.write_text('{"previous": true}\n', encoding="utf-8")
        with mock.patch.object(ygoDocGen, "render_text",
                               side_effect=RuntimeError("boom")):
            code, out, err = run(["--dir", str(self.dir), "--json", str(target)])
        self.assertEqual(code, 1)
        self.assertEqual(target.read_text(encoding="utf-8"), '{"previous": true}\n')
        self.assertIn("previous document is still intact", err)
        self.assertEqual(list(self.dir.glob("*.tmp")), [])
        self.assertEqual(list(self.dir.glob("*.json.*")), [])

    def test_successful_json_is_complete_and_reparses(self):
        target = self.dir / "docs.json"
        code, out, err = run(["--dir", str(self.dir), "--json", str(target)])
        self.assertEqual(code, 0, err)
        data = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(len(data["functions"]), 9)
        self.assertEqual(data["counts"]["functions"], 9)
        self.assertEqual(data["missing_sources"], [])

    def test_partial_checkout_warns_and_still_documents(self):
        """Generation is allowed to be partial; a check must not call it clean."""
        (self.dir / "libgroup.cpp").unlink()
        code, out, err = run(["--dir", str(self.dir)])
        self.assertEqual(code, 0)
        self.assertIn("incomplete sources", err)
        self.assertIn("missing libgroup.cpp", err)
        code2, out2, err2 = run(["--dir", str(self.dir), "--check"])
        self.assertEqual(code2, 1)
        self.assertIn("missing source file: libgroup.cpp", out2)

    def test_complete_subdirectory_beats_a_stray_partial_copy(self):
        """A stray `libcard.cpp` at the root must not truncate the document.

        Real layouts have the sources in `<checkout>/ocgcore` (or `src`); if a
        single binding file also sits at the top level, the complete set is the
        one to read, and the choice has to be visible on stderr.
        """
        full = self.dir / "ocgcore"
        full.mkdir()
        for name in ("libcard.cpp", "libduel.cpp", "libeffect.cpp",
                     "libgroup.cpp", "libdebug.cpp"):
            (full / name).write_bytes((self.dir / name).read_bytes())
        # Now put a partial copy in the root: only the card library.
        for name in ("libduel.cpp", "libeffect.cpp", "libgroup.cpp", "libdebug.cpp"):
            (self.dir / name).unlink()
        code, out, err = run(["--dir", str(self.dir)])
        self.assertEqual(code, 0, err)
        self.assertIn("reading the more complete set in", err)
        self.assertNotIn("incomplete sources", err)
        self.assertIn("Card.GetOriginalCode", out)
        self.assertIn("Duel.", out)
        checks = run(["--dir", str(self.dir), "--check"])
        self.assertEqual(checks[0], 0, checks[1] + checks[2])
        self.assertIn("functions: 9", checks[1])

    def test_missing_sources_are_named_in_the_json(self):
        (self.dir / "libdebug.cpp").write_text(LIBDEBUG_BROKEN, encoding="utf-8")
        self.doc("--json", str(self.dir / "out.json"))
        # Remove one file after the fact to model a partial checkout.
        (self.dir / "libduel.cpp").unlink()
        code, out, err = run(["--dir", str(self.dir), "--json", str(self.dir / "out2.json")])
        data = json.loads((self.dir / "out2.json").read_text(encoding="utf-8"))
        self.assertIn("libduel.cpp", data["missing_sources"])


class TestCheck(Fixture):
    def test_clean_sources_pass(self):
        code, out, err = run(["--dir", str(self.dir), "--check"])
        self.assertEqual(code, 0)
        self.assertIn("defects: 0", out)

    def test_registration_without_a_body_is_a_defect(self):
        (self.dir / "libdebug.cpp").write_text(LIBDEBUG_BROKEN, encoding="utf-8")
        code, out, err = run(["--dir", str(self.dir), "--check"])
        self.assertEqual(code, 1)
        self.assertIn("debug_show_hint", out)

    def test_unreadable_argument_is_a_warning_and_strict_fails(self):
        # A warning is a field the tool could not infer; it must not be a
        # defect, but --strict has to treat it as one.  The fixture stays
        # complete, so the only finding is the unread argument itself.
        (self.dir / "libduel.cpp").write_text(LIBSTRICT, encoding="utf-8")
        code, out, err = run(["--dir", str(self.dir), "--check"])
        self.assertEqual(code, 0)
        self.assertIn("defects: 0", out)
        self.assertIn("argument 1 has no readable type", out)
        code2, out2, err2 = run(["--dir", str(self.dir), "--check", "--strict"])
        self.assertEqual(code2, 1)

    def test_strict_alone_is_an_error_not_a_document(self):
        """`--strict` only qualifies a check; alone it must not print output."""
        code, out, err = run(["--dir", str(self.dir), "--strict"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("--strict only modifies --check", err)

    def test_empty_directory_is_exit_two(self):
        empty = self.dir / "empty"
        empty.mkdir()
        code, out, err = run(["--dir", str(empty), "--check"])
        self.assertEqual(code, 2)
        self.assertIn("no binding sources", err)


class TestConsoleEncoding(Fixture):
    """A redirected Windows console gets a code page that may lack `●`.

    cp1252 cannot encode U+25CF: before the fix the run died at the first
    entry, and only after --json had already been written.
    """

    def invoke(self, encoding, extra=()):
        env = dict(os.environ, PYTHONIOENCODING=encoding)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "ygoDocGen.py"), "--dir", str(self.dir)]
            + list(extra),
            capture_output=True, env=env)
        return proc.returncode, proc.stdout, proc.stderr

    def test_cp1252_still_prints_the_whole_document_as_utf8(self):
        code, raw, err = self.invoke("cp1252")
        self.assertEqual(code, 0, err.decode("utf-8", "backslashreplace"))
        text = raw.decode("utf-8")
        self.assertEqual(len(text.splitlines()), 9)
        self.assertTrue(text.startswith("\u25cf"), "the marker survived the write")
        self.assertIn(b"writing UTF-8", err)

    def test_cp1252_with_json_delivers_both_outputs_completely(self):
        target = self.dir / "docs.json"
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "ygoDocGen.py"), "--dir", str(self.dir),
             "--json", str(target)], capture_output=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(len(proc.stdout.decode("utf-8").splitlines()), 9)
        data = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(len(data["functions"]), 9)

    def test_stdlib_failure_still_keeps_the_previous_document(self):
        """If stdout genuinely cannot be written, no JSON may be left behind."""
        target = self.dir / "docs.json"
        target.write_text('{"previous": true}\n', encoding="utf-8")
        with mock.patch.object(ygoDocGen, "setup_stdio",
                               side_effect=UnicodeEncodeError("charmap", "\u25cf", 0, 1,
                                                              "undefined")):
            code, out, err = run(["--dir", str(self.dir), "--json", str(target)])
        self.assertEqual(code, 1)
        self.assertEqual(target.read_text(encoding="utf-8"), '{"previous": true}\n')
        self.assertIn("previous document is still intact", err)

    def test_help_text_is_ascii_so_it_prints_on_any_code_page(self):
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        proc = subprocess.run([sys.executable, str(ROOT / "ygoDocGen.py"), "--help"],
                              capture_output=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc.stdout.decode("cp1252")


class TestDeterminism(Fixture):
    def test_output_does_not_depend_on_the_hash_seed(self):
        digests = set()
        for seed in ("0", "1", "12345"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            proc = subprocess.run(
                [sys.executable, str(ROOT / "ygoDocGen.py"), "--dir", str(self.dir)],
                capture_output=True, text=True, env=env, check=True)
            digests.add(proc.stdout)
        self.assertEqual(len(digests), 1)


@unittest.skipUnless(CORPUS and (CORPUS / "libcard.cpp").is_file(),
                     "no ocgcore checkout found (set YGODOCGEN_CORPUS to one)")
class TestRealCorpus(unittest.TestCase):
    """The claims in the README, measured on the real sources."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "doc.txt"
        cls.json = Path(cls.tmp.name) / "doc.json"
        code, stdout, stderr = run(["--dir", str(CORPUS), "--json", str(cls.json)])
        assert code == 0, stderr
        cls.out.write_text(stdout, encoding="utf-8")
        cls.data = json.loads(cls.json.read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_registration_count(self):
        """Pinned counts at the documented commit; invariants anywhere else."""
        data = self.data
        total = data["counts"]["functions"]
        sources = data["sources"]
        self.assertEqual(total, sum(s["registrations"] for s in sources),
                         "the total must be the sum of the per-library tables")
        self.assertEqual(sorted(s["namespace"] for s in sources),
                         sorted(PINNED_COUNTS), "the five binding libraries are all present")
        if corpus_fingerprint(CORPUS) == PINNED_FINGERPRINT \
                or corpus_commit(CORPUS) == PINNED_COMMIT:
            self.assertEqual(total, PINNED_TOTAL)
            for source in sources:
                self.assertEqual(source["registrations"],
                                 PINNED_COUNTS[source["namespace"]], source["file"])
        else:
            # A newer or older checkout: report the actual composition instead
            # of asserting a number from another revision.
            print("\nnote: %s is not the pinned revision; %d registrations (%s)"
                  % (CORPUS, total,
                     ", ".join("%s %d" % (s["namespace"], s["registrations"])
                               for s in sources)), file=sys.stderr)

    def test_no_structural_defects(self):
        code, out, err = run(["--dir", str(CORPUS), "--check"])
        self.assertEqual(code, 0)
        self.assertIn("defects: 0", out)

    def quoted_readme_examples(self):
        """Every `●` line the README shows, as the document would print it."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        quoted = set()
        for line in readme.splitlines():
            stripped = line.strip()
            if stripped.startswith("●"):
                quoted.add(stripped.rstrip("|").strip().replace("\\|", "|"))
            for cell in re.findall(r"`(●[^`]+)`", line):
                # A markdown table escapes a bare `|` as `\|`; that escape is
                # the table's, not part of the line the tool prints.
                quoted.add(cell.strip().replace("\\|", "|"))
        return quoted

    def test_readme_examples_are_verbatim_output(self):
        """Every `●` example in the README must exist in the generated document.

        The README quotes real lines to explain the notation; a wording change
        in the tool would silently make those quotes fiction.  Those lines are
        also a claim about one revision: a newer checkout may add a binding or
        an optional argument, so the exact text is required only for the pinned
        revision, while the namesake binding has to exist anywhere.
        """
        quoted = self.quoted_readme_examples()
        self.assertGreaterEqual(len(quoted), 5, "the README should show real lines")
        generated = set(self.out.read_text(encoding="utf-8").splitlines())
        if is_pinned(CORPUS):
            missing = sorted(q for q in quoted if q not in generated)
            self.assertEqual(missing, [],
                             "README quotes lines the tool no longer prints")
        else:
            have = {r["name"] for r in self.data["functions"]}
            gone = sorted(q for q in quoted
                          if re.match(r"●\S+ (\S+)\(", q)
                          and re.match(r"●\S+ (\S+)\(", q).group(1) not in have)
            self.assertEqual(gone, [],
                             "README explains a binding this checkout lacks")

    def test_readme_json_sample_is_the_live_record(self):
        """The README claims this block *is* the output; make that true.

        Hand-typed JSON in a README goes stale silently: the sample here had
        an argument with only half of its evidence and an empty field the tool
        no longer emits.  Comparing the parsed block with the live record means
        any change to the record shape fails the suite instead of the reader.
        """
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        block = re.search(r"```json\n(\{\"name\": \"Card.GetLinkedZone\".*?)```",
                          readme, re.S)
        self.assertIsNotNone(block, "the README lost its Card.GetLinkedZone sample")
        sample = json.loads(" ".join(block.group(1).split()))
        live = next(r for r in self.data["functions"]
                    if r["name"] == "Card.GetLinkedZone")
        if is_pinned(CORPUS):
            self.assertEqual(sample, live)
        else:
            # `table_index` and any argument added upstream are facts about a
            # revision, not about the record's shape; the shape is what this
            # sample teaches, so require the same keys and the same identity.
            self.assertEqual(sorted(sample), sorted(live),
                             "the documented record shape changed")
            for key in ("name", "lua_name", "symbol", "namespace", "file",
                        "return_arity"):
                self.assertEqual(sample[key], live[key])

        # The second sample shows only the arity fields; compare those, so a
        # renamed or dropped key fails here too.
        block = re.search(r"```json\n(\{\"name\": \"Duel.GetChainInfo\".*?)```",
                          readme, re.S)
        self.assertIsNotNone(block, "the README lost its Duel.GetChainInfo sample")
        sample = json.loads(" ".join(block.group(1).split()))
        chain = next(r for r in self.data["functions"]
                     if r["name"] == "Duel.GetChainInfo")
        self.assertEqual(sample, {k: chain[k] for k in sample})

    def test_names_match_the_registration_table(self):
        """Every name comes from the luaL_Reg table, one entry per registration."""
        records = self.data["functions"]
        names = [r["name"] for r in records]
        self.assertEqual(len(names), len(set(names)), "no duplicate Lua names")
        self.assertTrue(all(r["table"] and r["symbol"] for r in records))
        lua = {r["symbol"]: r["lua_name"] for r in records}
        self.assertEqual(lua["card_get_origin_code"], "GetOriginalCode")
        self.assertEqual(lua["card_get_linked_zone"], "GetLinkedZone")
        for record in records:
            self.assertTrue(record["name"].startswith(record["namespace"] + "."),
                            "%s is in namespace %s" % (record["name"], record["namespace"]))
            self.assertNotEqual(record["return"], "?", record["name"])

    def test_every_evidence_string_is_a_quote_or_marked_derived(self):
        """The provenance promise, checked against the whole real corpus.

        On the fixture this is a sample; here it covers several thousand
        strings, so an inference that forgets the `derived:` prefix (or a
        paraphrase that drifts from the source) fails the suite.
        """
        sources = {}
        for name in ygoDocGen.LIB_FILES:
            path = Path(CORPUS) / name
            if path.is_file():
                sources[name] = " ".join(
                    path.read_text(encoding="utf-8", errors="replace").split())
        quoted = derived_count = 0
        for record in self.data["functions"]:
            source = sources[record["file"]]
            for text in ([record["min_evidence"]] + record["return_evidence"]
                         + [e for a in record["args"] for e in a["evidence"]]):
                if text.startswith(ygoDocGen.DERIVED):
                    derived_count += 1
                    continue
                self.assertIn(" ".join(text.split()), source,
                              "%s cites %r, which is not in %s"
                              % (record["name"], text, record["file"]))
                quoted += 1
        self.assertGreater(quoted, 1000, "most evidence must be a real quote")
        self.assertLess(derived_count, quoted, "quotes should dominate inferences")

    def test_dynamic_arity_is_reported_for_toss_coin(self):
        toss = next(r for r in self.data["functions"] if r["name"] == "Duel.TossCoin")
        self.assertEqual(toss["return_arity"], "input-dependent")
        self.assertIn("~int...", toss["return"])

    def test_fixed_arity_is_reported_for_announce_number(self):
        rec = next(r for r in self.data["functions"] if r["name"] == "Duel.AnnounceNumber")
        self.assertEqual(rec["return_arity"], "fixed")
        self.assertEqual(rec["return"], "~int,int")

    def test_readme_merge_table_is_the_live_merge(self):
        """The five counts under `--annotations` must match a real merge.

        Those numbers were hand-written facts about one file and one checkout:
        nothing recomputed them, so a change in the parser or in
        `new_functions.txt` would have left the README quietly wrong about how
        much of the hand-written document survives.
        """
        annotations = ROOT / "new_functions.txt"
        if not annotations.is_file():
            self.skipTest("new_functions.txt is not in this copy of the repo")
        code, out, err = run(["--dir", str(CORPUS),
                              "--annotations", str(annotations)])
        self.assertEqual(code, 0, err)
        blocks, encoding, warnings = ygoDocGen.read_annotations(annotations)
        self.assertIn("%d annotation blocks" % len(blocks), err)
        self.assertEqual(encoding, "gb18030",
                         "new_functions.txt is gb18030; its bytes are what "
                         "DataEditorX ships, so a re-encode must fail here")
        names = {r["name"] for r in self.data["functions"]}
        keys = {b["key"] for b in blocks}
        live = {
            "annotation blocks read": len(blocks),
            "matched to a binding, emitted verbatim": len(names & keys),
            "bindings with no block, printed generated": len(names - keys),
            "stale C++-derived line inside a block, dropped":
                sum(len(b["dropped"]) for b in blocks),
            "blocks with no binding, kept at the end": len(keys - names),
        }
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for label in live:
            self.assertIsNotNone(
                re.search(r"\|\s*%s\s*\|\s*(\d+)\s*\|" % re.escape(label),
                          readme), "the README lost its merge-table row %r" % label)
        if not is_pinned(CORPUS):
            # The merge is real everywhere; only the exact counts belong to
            # the pinned revision, so report them instead of asserting them.
            print("\nnote: %s is not the pinned revision; merged %d blocks into "
                  "%d bindings, %d kept without one, %d stale lines dropped"
                  % (CORPUS, live["annotation blocks read"],
                     live["matched to a binding, emitted verbatim"],
                     live["blocks with no binding, kept at the end"],
                     live["stale C++-derived line inside a block, dropped"]),
                  file=sys.stderr)
            return
        markers = sum(1 for l in out.splitlines()
                      if l.lstrip().startswith("\u25cf"))
        self.assertEqual(markers, 654, "the merged document's entry count")
        for label, measured in live.items():
            match = re.search(r"\|\s*%s\s*\|\s*(\d+)\s*\|"
                              % re.escape(label), readme)
            self.assertEqual(int(match.group(1)), measured,
                             "README row %r is stale" % label)


if __name__ == "__main__":
    unittest.main()
