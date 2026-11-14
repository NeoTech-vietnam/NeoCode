#!/usr/bin/env python3
"""Offline end-to-end check of the practice tooling.

    python tools/selftest.py

Everything happens in a temporary root that is removed at the end: throwaway sample
problems (adding two integers and a few deliberate bugs, not LeetCode solutions) are
created with new_problem.py and built/run with build_test.py. --fetch is exercised
with a canned GraphQL response, so no network access is needed. The repo's c/ and
cpp/ trees are never touched. Sanitizer cases are skipped when the compiler has no
sanitizer support (e.g. MinGW GCC 6.3). Every command and its full output is written
to build/selftest.log (gitignored) for diagnosis.
"""

import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
sys.path.insert(0, TOOLS_DIR)
sys.dont_write_bytecode = True  # keep tools/__pycache__ out of the repo

import build_test  # noqa: E402
import new_problem  # noqa: E402

LOG_PATH = os.path.join(REPO_ROOT, "build", "selftest.log")  # build/ is gitignored
LOG = []

SAMPLE_ID = "9999"
SAMPLE_SLUG = "selftest-add"
SAMPLE_DIR = "9999_selftest-add"

CANNED_RESPONSE = {
    "data": {
        "question": {
            "questionFrontendId": "9999",
            "title": "Selftest Add",
            "isPaidOnly": False,
            "codeSnippets": [
                {"lang": "C", "langSlug": "c", "code": (
                    "/**\r\n"
                    " * Definition for singly-linked list.\r\n"
                    " * struct ListNode {\r\n"
                    " *     int val;\r\n"
                    " *     struct ListNode *next;\r\n"
                    " * };\r\n"
                    " */\r\n"
                    "int add(int a, int b) {\r\n"
                    "    \r\n"
                    "}")},
                {"lang": "C++", "langSlug": "cpp", "code": (
                    "class Solution {\n"
                    "public:\n"
                    "    int add(int a, int b) {\n"
                    "        \n"
                    "    }\n"
                    "};")},
            ],
            "exampleTestcaseList": ["2\n3", "-1\n1"],
            "metaData": json.dumps({
                "name": "add",
                "params": [{"name": "a", "type": "integer"}, {"name": "b", "type": "integer"}],
                "return": {"type": "integer"},
            }),
            "content": (
                "<p>Return <code>a + b</code>.</p>\n"
                "<p><strong>Example 1:</strong></p>\n"
                "<pre>\n<strong>Input:</strong> a = 2, b = 3\n<strong>Output:</strong> 5\n</pre>\n"
                "<p><strong>Example 2:</strong></p>\n"
                "<pre>\n<strong>Input:</strong> a = -1, b = 1\n<strong>Output:</strong> 0\n</pre>\n"
            ),
        }
    }
}

C_ADD_SOLUTION = """\
int add(int a, int b) {
    return a + b;
}
"""

C_ADD_CHECKS = """\
    LC_CHECK(add(2, 3) == 5);
    LC_CHECK(add(-1, 1) == 0);
    int values[] = {1, 2, 3};
    int other[] = {1, 2, 4};
    struct ListNode *list = lc_list_from_array(values, 3);
    LC_CHECK(lc_list_equals_array(list, values, 3));
    LC_CHECK(!lc_list_equals_array(list, values, 2));
    lc_list_free(list);
    int level[] = {1, LC_NULL, 2, 3};
    struct TreeNode *root = lc_tree_from_level(level, 4);
    LC_CHECK(root != NULL && root->val == 1 && root->left == NULL && root->right != NULL);
    LC_CHECK(root->right->val == 2 && root->right->left != NULL && root->right->left->val == 3);
    lc_tree_free(root);
    LC_CHECK(lc_int_array_equals(values, 3, values, 3));
    LC_CHECK(!lc_int_array_equals(values, 3, other, 3));
"""

CPP_ADD_SOLUTION = """\
class Solution {
public:
    int add(int a, int b) {
        return a + b;
    }
};
"""

CPP_ADD_CHECKS = """\
    Solution solution;
    LC_CHECK(solution.add(2, 3) == 5);
    ListNode *list = lc_list_from_array(vector<int>{1, 2, 3});
    LC_CHECK(lc_list_equals_array(list, vector<int>{1, 2, 3}));
    LC_CHECK(!lc_list_equals_array(list, vector<int>{1, 2}));
    lc_list_free(list);
    TreeNode *root = lc_tree_from_level(vector<int>{1, LC_NULL, 2});
    LC_CHECK(root != nullptr && root->left == nullptr && root->right != nullptr && root->right->val == 2);
    lc_tree_free(root);
    LC_CHECK(lc_int_array_equals(vector<int>{1, 2}, vector<int>{1, 2}));
"""

C_BUILD_ERROR_SOLUTION = """\
int add(int a, int b) {
    int unused = 0;
    return a + b;
}
"""

# Deliberate memory bugs; volatile keeps the compiler from flagging them at build time.
C_HEAP_OVERFLOW_SOLUTION = """\
int poke(int index) {
    volatile int i = index;
    int *p = (int *)malloc(2 * sizeof *p);
    if (p == NULL) {
        return -1;
    }
    p[i] = 7;
    int value = p[i];
    free(p);
    return value;
}
"""

C_USE_AFTER_FREE_SOLUTION = """\
int stale(void) {
    int *p = (int *)malloc(sizeof *p);
    if (p == NULL) {
        return -1;
    }
    *p = 5;
    int *volatile alias = p;
    free(p);
    return *alias;
}
"""


class SelfTest:
    def __init__(self):
        self.failures = 0

    def check(self, name, ok, output=""):
        if ok:
            say("PASS  " + name)
        else:
            self.failures += 1
            say("FAIL  " + name)
            if output:
                say(build_test.indent_head(output, 40))
        return bool(ok)

    def skip(self, name, reason):
        say("SKIP  %s (%s)" % (name, reason))


def say(text=""):
    """Print a line and keep it for the log file."""
    print(text)
    sys.stdout.flush()
    LOG.append(text)


def write_log():
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        write(LOG_PATH, "\n".join(LOG) + "\n")
        print("Full log (every command and its output): " + LOG_PATH)
    except OSError as e:
        print("WARN  could not write %s: %s" % (LOG_PATH, e))


def run_tool(script, args, extra_env=None):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env.pop("LC_GRAPHQL_URL", None)
    if extra_env:
        env.update(extra_env)
    cmd = [sys.executable, os.path.join(TOOLS_DIR, script)] + list(args)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, timeout=900)
    output = proc.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    LOG.append("$ %s %s  [exit %d]\n%s" % (script, " ".join(args), proc.returncode, output.rstrip()))
    return proc.returncode, output


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def snapshot_dir(path):
    """Map relative file path -> bytes for every file under path."""
    result = {}
    for dirpath, _, filenames in os.walk(path):
        for name in filenames:
            full = os.path.join(dirpath, name)
            with open(full, "rb") as f:
                result[os.path.relpath(full, path)] = f.read()
    return result


def snapshot_repo_problems():
    result = {}
    for top in ("c", "cpp"):
        for rel, data in snapshot_dir(os.path.join(REPO_ROOT, top)).items():
            result[os.path.join(top, rel)] = data
    return result


def insert_checks(test_path, checks):
    text = read(test_path)
    anchor = "    return lc_finish();"
    if anchor not in text:
        raise AssertionError("%s has no '%s' line" % (test_path, anchor.strip()))
    write(test_path, text.replace(anchor, checks + anchor, 1))


def create_problem(t, root, topic, pid, slug, lang="c"):
    args = [topic, pid, slug, "--root", root] + (["--lang", lang] if lang != "c" else [])
    code, out = run_tool("new_problem.py", args)
    path = os.path.join(root, lang, topic, "%s_%s" % (pid, slug))
    t.check("new_problem creates %s/%s/%s_%s" % (lang, topic, pid, slug), code == 0 and os.path.isdir(path), out)
    return path


def status_line(status, rel):
    return re.compile(r"^%s\s+%s\b" % (re.escape(status), re.escape(rel)), re.M)


def step_create(t, root):
    for lang in ("c", "cpp"):
        names = new_problem.LANGS[lang]
        d = create_problem(t, root, "big-o", SAMPLE_ID, SAMPLE_SLUG, lang)
        files = ("notes.md", names["solution"], names["test"])
        if not t.check("%s problem has notes.md, %s and %s" % (lang, names["solution"], names["test"]),
                       all(os.path.isfile(os.path.join(d, f)) for f in files)):
            continue
        notes = read(os.path.join(d, "notes.md"))
        t.check("%s notes.md placeholders filled in" % lang,
                all(p not in notes for p in ("<id>", "<slug>", "<Problem title>"))
                and "# 9999. Selftest Add" in notes
                and "https://leetcode.com/problems/selftest-add/" in notes, notes)
        solution = read(os.path.join(d, names["solution"]))
        t.check("%s solution is a paste-ready TODO stub (no main, no tests)" % lang,
                "main(" not in solution and "LC_CHECK" not in solution and "TODO" in solution, solution)
        test_src = read(os.path.join(d, names["test"]))
        t.check("%s test file includes lc.h and the solution and ends with lc_finish()" % lang,
                '#include "lc.h"' in test_src and '#include "%s"' % names["solution"] in test_src
                and "return lc_finish();" in test_src and "TODO: add your own test cases" in test_src,
                test_src)
        t.check("%s files use LF line endings" % lang,
                all(b"\r" not in data for data in snapshot_dir(d).values()))


def step_refuse(t, root):
    code, out = run_tool("new_problem.py", ["dynamic-programming", "9998", "x", "--root", root])
    t.check("unknown topic refused",
            code != 0 and "unknown topic" in out and not os.path.exists(os.path.join(root, "c", "dynamic-programming")),
            out)
    code, out = run_tool("new_problem.py", ["big-o", "9998", "Bad_Slug", "--root", root])
    t.check("invalid slug refused",
            code != 0 and not os.path.exists(os.path.join(root, "c", "big-o", "9998_Bad_Slug")), out)
    code, out = run_tool("new_problem.py", ["big-o", "0", "zero-id", "--root", root])
    t.check("non-positive id refused",
            code != 0 and not os.path.exists(os.path.join(root, "c", "big-o", "0000_zero-id")), out)
    d = os.path.join(root, "c", "big-o", SAMPLE_DIR)
    before = snapshot_dir(d)
    code, out = run_tool("new_problem.py", ["big-o", SAMPLE_ID, SAMPLE_SLUG, "--root", root])
    t.check("existing problem directory refused and left byte-identical",
            code != 0 and "already exists" in out and snapshot_dir(d) == before, out)


def step_fresh_skeletons(t, root):
    code, out = run_tool("build_test.py", ["--root", root])
    t.check("fresh skeletons build and report NO TESTS (exit 0)",
            code == 0 and status_line("NO TESTS", "c/big-o/" + SAMPLE_DIR).search(out)
            and status_line("NO TESTS", "cpp/big-o/" + SAMPLE_DIR).search(out), out)
    t.check("startup header lists the C and C++ compilers",
            "C compiler:" in out and "C++ compiler:" in out and "[-std=c11" in out, out)
    match = re.search(r"C\+\+ compiler:.*?\[(-std=[^\]\s]+)", out)
    t.check("C++ standard probe picked a valid flag",
            match is not None and match.group(1) in build_test.CXX_STD_CANDIDATES, out)
    code, out = run_tool("build_test.py", ["--root", root, "--strict"])
    t.check("--strict fails on NO TESTS (exit 1)", code == 1, out)


def raises_fetch_error(func, *args):
    try:
        func(*args)
    except new_problem.FetchError:
        return True
    return False


def step_parse(t):
    q = new_problem.parse_question(CANNED_RESPONSE, "c")
    t.check("parse_question reads id, title and the C snippet",
            q["id"] == "9999" and q["title"] == "Selftest Add" and "int add(int a, int b)" in q["snippet"]
            and "\r" not in q["snippet"], repr(q))
    t.check("parse_question labels examples with parameter names and outputs",
            q["examples"] == ["a = 2, b = 3 -> 5", "a = -1, b = 1 -> 0"], repr(q["examples"]))
    marked = new_problem.add_todo_marker(q["snippet"])
    t.check("TODO marker goes into the empty function body",
            "\n    // TODO: write your solution\n" in marked
            and marked.index("TODO") > marked.index("int add(") and "struct ListNode" in marked, marked)
    q = new_problem.parse_question(CANNED_RESPONSE, "cpp")
    marked = new_problem.add_todo_marker(q["snippet"])
    t.check("parse_question reads the C++ snippet",
            "class Solution" in q["snippet"] and "\n        // TODO: write your solution\n" in marked, marked)
    paid = copy.deepcopy(CANNED_RESPONSE)
    paid["data"]["question"]["isPaidOnly"] = True
    t.check("premium problems are rejected", raises_fetch_error(new_problem.parse_question, paid, "c"))
    t.check("missing snippet is rejected", raises_fetch_error(new_problem.parse_question, CANNED_RESPONSE, "rust"))
    t.check("unknown problem is rejected",
            raises_fetch_error(new_problem.parse_question, {"data": {"question": None}}, "c"))


def step_fetch(t, root):
    canned_path = os.path.join(root, "canned_graphql.json")
    write(canned_path, json.dumps(CANNED_RESPONSE))
    url = Path(canned_path).as_uri()
    for lang in ("c", "cpp"):
        names = new_problem.LANGS[lang]
        args = ["bit", SAMPLE_ID, SAMPLE_SLUG, "--fetch", "--root", root] + (["--lang", lang] if lang != "c" else [])
        code, out = run_tool("new_problem.py", args, {"LC_GRAPHQL_URL": url})
        d = os.path.join(root, lang, "bit", SAMPLE_DIR)
        if not t.check("--fetch with canned JSON creates %s problem" % lang,
                       code == 0 and "fetch failed" not in out and os.path.isfile(os.path.join(d, names["test"])),
                       out):
            continue
        solution = read(os.path.join(d, names["solution"]))
        t.check("%s solution is the fetched signature with a TODO body" % lang,
                "int add(int a, int b)" in solution and "TODO: write your solution" in solution
                and "main(" not in solution and "return a + b" not in solution, solution)
        test_src = read(os.path.join(d, names["test"]))
        t.check("%s test file has the examples as comments" % lang,
                "    //   a = 2, b = 3 -> 5\n" in test_src and "    //   a = -1, b = 1 -> 0\n" in test_src, test_src)
    bit_dir = os.path.join(root, "c", "bit")
    code, out = run_tool("build_test.py", [bit_dir, "--root", root])
    t.check("fetched stub reports TODO (exit 0)",
            code == 0 and status_line("TODO", "c/bit/" + SAMPLE_DIR).search(out), out)
    code, out = run_tool("build_test.py", [bit_dir, "--root", root, "--strict"])
    t.check("--strict fails on TODO (exit 1)", code == 1, out)


def step_fetch_fallback(t, root):
    # Port 9 on localhost is closed, so the request fails without touching the network.
    code, out = run_tool("new_problem.py", ["memory", SAMPLE_ID, SAMPLE_SLUG, "--fetch", "--root", root],
                         {"LC_GRAPHQL_URL": "http://127.0.0.1:9/graphql", "NO_PROXY": "127.0.0.1,localhost",
                          "no_proxy": "127.0.0.1,localhost"})
    solution = os.path.join(root, "c", "memory", SAMPLE_DIR, "solution.c")
    t.check("--fetch failure falls back to the offline skeleton with a message",
            code == 0 and "fetch failed" in out and "using offline skeleton" in out
            and os.path.isfile(solution) and "int solution(void)" in read(solution), out)


def step_pass(t, root):
    c_dir = os.path.join(root, "c", "big-o", SAMPLE_DIR)
    cpp_dir = os.path.join(root, "cpp", "big-o", SAMPLE_DIR)
    write(os.path.join(c_dir, "solution.c"), C_ADD_SOLUTION)
    insert_checks(os.path.join(c_dir, "test.c"), C_ADD_CHECKS)
    write(os.path.join(cpp_dir, "solution.cpp"), CPP_ADD_SOLUTION)
    insert_checks(os.path.join(cpp_dir, "test.cpp"), CPP_ADD_CHECKS)

    code, out = run_tool("build_test.py", ["--root", root])
    t.check("all-problems run: add sample and lc.h helpers PASS in C and C++ (exit 0)",
            code == 0 and status_line("PASS", "c/big-o/" + SAMPLE_DIR).search(out)
            and status_line("PASS", "cpp/big-o/" + SAMPLE_DIR).search(out), out)
    code, out = run_tool("build_test.py", ["c/big-o/" + SAMPLE_DIR, "--root", root])
    t.check("single-problem run, path relative to the root (C)",
            code == 0 and status_line("PASS", "c/big-o/" + SAMPLE_DIR).search(out) and " 1 total" in out, out)
    code, out = run_tool("build_test.py", [cpp_dir, "--root", root])
    t.check("single-problem run, absolute path (C++)",
            code == 0 and status_line("PASS", "cpp/big-o/" + SAMPLE_DIR).search(out) and " 1 total" in out, out)


def step_failures(t, root):
    d = create_problem(t, root, "pointer", "9999", "selftest-fail")
    write(os.path.join(d, "solution.c"), C_ADD_SOLUTION)
    insert_checks(os.path.join(d, "test.c"), "    LC_CHECK(add(2, 2) == 5);\n")
    code, out = run_tool("build_test.py", [d, "--root", root])
    t.check("failing check reports TEST FAIL (exit 1)",
            code == 1 and status_line("TEST FAIL", "c/pointer/9999_selftest-fail").search(out)
            and "add(2, 2) == 5" in out, out)

    d = create_problem(t, root, "pointer", "9998", "selftest-build-fail")
    write(os.path.join(d, "solution.c"), C_BUILD_ERROR_SOLUTION)
    code, out = run_tool("build_test.py", [d, "--root", root])
    t.check("compile error reports BUILD FAIL (exit 1)",
            code == 1 and status_line("BUILD FAIL", "c/pointer/9998_selftest-build-fail").search(out), out)

    code, out = run_tool("build_test.py", [os.path.join(root, "c", "no-such-topic"), "--root", root])
    t.check("unknown PATH exits non-zero", code != 0 and "no problems under" in out, out)


def step_output_location(t, root):
    exe = os.path.join(root, "build", "c", "big-o", SAMPLE_DIR, "test" + build_test.EXE)
    t.check("build output goes to <root>/build/",
            os.path.isfile(exe) and not os.path.exists(os.path.join(REPO_ROOT, "build", "c", "big-o", SAMPLE_DIR)))


def step_select_compiler(t):
    def which(*names):
        return lambda name: "/fake/bin/" + name if name in names else None

    def always(_):
        return True

    def never(_):
        return False

    select = build_test.select_compiler
    msys2_cxx = build_test.MSYS2_CLANG64_BIN + "\\clang++.exe"
    cases = [
        ("CC wins", select("c", {"CC": "my-cc"}, which("clang", "gcc"), always, True)[0] == "my-cc"),
        ("CXX wins", select("cpp", {"CXX": "my-cxx"}, which("clang++", "g++"), always, True)[0] == "my-cxx"),
        ("clang on PATH beats CLANG64 and gcc",
         select("c", {}, which("clang", "gcc"), always, True)[0] == "/fake/bin/clang"),
        ("CLANG64 beats g++ on Windows", select("cpp", {}, which("g++"), always, True)[0] == msys2_cxx),
        ("CLANG64 ignored off Windows", select("c", {}, which("gcc"), always, False)[0] == "/fake/bin/gcc"),
        ("gcc when CLANG64 is not installed", select("c", {}, which("gcc"), never, True)[0] == "/fake/bin/gcc"),
        ("candidate failing the probe is skipped",
         select("c", {}, which("clang", "gcc"), always, False,
                lambda cc: None if "clang" in cc else "-std=c11") == ("/fake/bin/gcc", "-std=c11")),
        ("nothing found", select("c", {}, which(), never, True) == (None, None)),
    ]
    for name, ok in cases:
        t.check("select_compiler: " + name, ok)


def step_sanitizers(t, root):
    try:
        build_test.detect_toolchain("c", sanitize=True)
        reason = ""
    except build_test.ToolError as e:
        reason = str(e).splitlines()[0]
    if reason:
        code, out = run_tool("build_test.py", ["--root", root, "--sanitize"])
        t.check("--sanitize without sanitizer support exits 2 with the MSYS2 CLANG64 hint",
                code == 2 and "MSYS2 CLANG64" in out, out)
        t.skip("sanitizer cases", reason)
        return

    c_dir = os.path.join(root, "c", "big-o", SAMPLE_DIR)
    code, out = run_tool("build_test.py", [c_dir, "--root", root, "--sanitize"])
    t.check("add sample PASSes under --sanitize",
            code == 0 and status_line("PASS", "c/big-o/" + SAMPLE_DIR).search(out), out)
    for pid, slug, solution, check in (
            ("9998", "selftest-heap-overflow", C_HEAP_OVERFLOW_SOLUTION, "    LC_CHECK(poke(2) == 7);\n"),
            ("9997", "selftest-use-after-free", C_USE_AFTER_FREE_SOLUTION, "    LC_CHECK(stale() == 5);\n")):
        d = create_problem(t, root, "memory", pid, slug)
        write(os.path.join(d, "solution.c"), solution)
        insert_checks(os.path.join(d, "test.c"), check)
        code, out = run_tool("build_test.py", [d, "--root", root, "--sanitize"])
        t.check("%s reported as SANITIZER (exit 1)" % slug,
                code == 1 and status_line("SANITIZER", "c/memory/%s_%s" % (pid, slug)).search(out), out)


def remove_tree(path):
    # Freshly built .exe files can be locked briefly on Windows (antivirus), so retry.
    for _ in range(10):
        if not os.path.exists(path):
            return
        shutil.rmtree(path, ignore_errors=True)
        if os.path.exists(path):
            time.sleep(0.5)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    t = SelfTest()
    repo_before = snapshot_repo_problems()
    root = tempfile.mkdtemp(prefix="lc-selftest-")
    say("Self-test root: " + root)
    say("Python %s on %s" % (sys.version.split()[0], sys.platform))
    steps = (
        lambda: step_create(t, root),
        lambda: step_refuse(t, root),
        lambda: step_fresh_skeletons(t, root),
        lambda: step_parse(t),
        lambda: step_fetch(t, root),
        lambda: step_fetch_fallback(t, root),
        lambda: step_pass(t, root),
        lambda: step_failures(t, root),
        lambda: step_output_location(t, root),
        lambda: step_select_compiler(t),
        lambda: step_sanitizers(t, root),
    )
    try:
        os.makedirs(os.path.join(root, "templates"))
        shutil.copyfile(os.path.join(REPO_ROOT, "templates", "notes.md"),
                        os.path.join(root, "templates", "notes.md"))
        for step in steps:
            # An unexpected error fails only its own step; later steps still run.
            try:
                step()
            except Exception:
                t.check("step ran without an unexpected error", False, traceback.format_exc())
    finally:
        remove_tree(root)
    t.check("repo c/ and cpp/ trees untouched", snapshot_repo_problems() == repo_before)
    if os.path.exists(root):
        say("WARN  could not fully remove %s (file still locked?)" % root)

    say()
    if t.failures:
        say("Self-test FAILED: %d check(s) failed" % t.failures)
    else:
        say("Self-test passed")
    write_log()
    return 1 if t.failures else 0


if __name__ == "__main__":
    sys.exit(main())
