#!/usr/bin/env python3
r"""Build and run the local tests of every practice problem, or only the given ones.

    python tools/build_test.py [PATH ...] [--root DIR] [--timeout S] [--strict] [--sanitize]

Each problem's test.c / test.cpp (which includes tools/lc.h and solution.c / solution.cpp)
is compiled into build/ and run. One status line is printed per problem, then a summary;
the exit code is 1 when a problem fails and 2 on usage or toolchain errors.

Compilers: $CC / $CXX if set, otherwise clang on PATH, then MSYS2 CLANG64
(C:\msys64\clang64\bin, Windows only), then gcc / g++.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # keep tools/__pycache__ out of the repo
from new_problem import CPP_HEADERS, C_HEADERS, LANGS  # noqa: E402

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(TOOLS_DIR)
IS_WINDOWS = os.name == "nt"
EXE = ".exe" if IS_WINDOWS else ""
MSYS2_CLANG64_BIN = r"C:\msys64\clang64\bin"

COMPILERS = {
    "c": {"name": "C", "label": "C compiler:", "env": "CC", "clang": "clang", "gcc": "gcc"},
    "cpp": {"name": "C++", "label": "C++ compiler:", "env": "CXX", "clang": "clang++", "gcc": "g++"},
}
WARN_FLAGS = ["-Wall", "-Wextra", "-Werror"]
C_STD = "-std=c11"
# -std=c++1z is how GCC 6 spells C++17.
CXX_STD_CANDIDATES = ["-std=c++20", "-std=c++17", "-std=c++1z"]
SANITIZE_FLAGS = ["-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-g"]
SANITIZER_MARKERS = (
    "ERROR: AddressSanitizer", "runtime error:", "SUMMARY: AddressSanitizer",
    "SUMMARY: UndefinedBehaviorSanitizer", "LeakSanitizer",
)
RESULT_RE = re.compile(r"LC-RESULT checks=(\d+) failed=(\d+)")
TODO_RE = re.compile(r"TODO:[^\n]*write your solution")
FAILED_STATUSES = ("BUILD FAIL", "TEST FAIL", "TIMEOUT", "SANITIZER")
BUILD_TIMEOUT = 120
PROBE_TIMEOUT = 60

C_PROBE = "".join("#include <%s>\n" % h for h in C_HEADERS) + (
    '#include "lc.h"\n'
    "\n"
    "int main(void) {\n"
    "    return lc_finish();\n"
    "}\n"
)
CPP_PROBE = "".join("#include <%s>\n" % h for h in CPP_HEADERS) + (
    "using namespace std;\n"
    '#include "lc.h"\n'
    "\n"
    "int main() {\n"
    "    vector<int> v{1, 2};\n"
    "    return lc_finish() + static_cast<int>(v.size()) - 2;\n"
    "}\n"
)
SANITIZE_PROBE_C = r"""#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = (int *)malloc(4 * sizeof *p);
    if (p == NULL) {
        return 1;
    }
    p[3] = 1;
    printf("%d\n", p[3]);
    free(p);
    return 0;
}
"""
SANITIZE_PROBE_CPP = r"""#include <cstdio>
#include <vector>

int main() {
    std::vector<int> v(4, 1);
    std::printf("%d\n", v[3]);
    return 0;
}
"""


class ToolError(Exception):
    pass


class Problem:
    def __init__(self, lang, topic, name, path):
        self.lang = lang
        self.topic = topic
        self.name = name
        self.path = path

    @property
    def rel(self):
        return "/".join((self.lang, self.topic, self.name))


class Toolchain:
    def __init__(self, kind, path, std_flags, version, env):
        self.kind = kind
        self.path = path
        self.std_flags = std_flags
        self.version = version
        self.env = env

    def describe(self):
        notes = []
        if "-std=c++1z" in self.std_flags:
            notes.append("C++17, GCC 6 spelling")
        note = " (%s)" % "; ".join(notes) if notes else ""
        return "%-13s %s [%s]%s  %s" % (COMPILERS[self.kind]["label"], self.path,
                                        " ".join(self.std_flags), note, self.version)


def run_cmd(cmd, env=None, cwd=None, timeout=None):
    """Run argv without a shell; return (exit code, stdout+stderr). May raise TimeoutExpired."""
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout)
    except OSError as e:
        return 127, str(e)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def indent_head(text, limit=40):
    lines = text.rstrip().splitlines()
    if len(lines) > limit:
        lines = lines[:limit] + ["... (%d more lines)" % (len(lines) - limit)]
    return "\n".join("    " + line for line in lines)


def tool_env(compiler, sanitize=False):
    """Environment for compiling and running. On Windows the compiler's bin directory goes
    first on PATH so its runtime DLLs (including the sanitizer runtime) are found."""
    env = dict(os.environ)
    if IS_WINDOWS:
        resolved = shutil.which(compiler) or compiler
        if os.path.dirname(resolved):
            env["PATH"] = os.path.dirname(os.path.abspath(resolved)) + os.pathsep + env.get("PATH", "")
    if sanitize:
        env["UBSAN_OPTIONS"] = "halt_on_error=1:print_stacktrace=1"
    return env


def try_build(compiler, flags, source, ext, env, run=False):
    """Compile (and optionally run) a tiny program in a temporary directory; return (ok, output)."""
    tmp = tempfile.mkdtemp(prefix="lc-probe-")
    try:
        src = os.path.join(tmp, "probe" + ext)
        exe = os.path.join(tmp, "probe" + EXE)
        with open(src, "w", encoding="utf-8", newline="\n") as f:
            f.write(source)
        try:
            code, output = run_cmd([compiler] + flags + [src, "-o", exe], env=env, timeout=PROBE_TIMEOUT)
            if code != 0 or not run:
                return code == 0, output
            code, run_output = run_cmd([exe], env=env, cwd=tmp, timeout=PROBE_TIMEOUT)
            return code == 0, output + run_output
        except subprocess.TimeoutExpired:
            return False, "probe timed out"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def select_compiler(kind, env, which, exists, is_windows, probe=None):
    """Pick the compiler for kind ("c" or "cpp"): $CC/$CXX if set, else clang on PATH, else
    MSYS2 CLANG64 (Windows only), else gcc/g++. Candidates must pass probe(compiler), whose
    result is returned with the compiler: (compiler, probe result) or (None, None)."""
    info = COMPILERS[kind]
    forced = (env.get(info["env"]) or "").strip()
    if forced:
        found = [which(forced) or forced]
    else:
        found = [which(info["clang"])]
        if is_windows:
            msys2 = MSYS2_CLANG64_BIN + "\\" + info["clang"] + ".exe"
            found.append(msys2 if exists(msys2) else None)
        found.append(which(info["gcc"]))
    candidates = []
    for compiler in found:
        if compiler and os.path.normcase(compiler) not in [os.path.normcase(c) for c in candidates]:
            candidates.append(compiler)
    for compiler in candidates:
        result = probe(compiler) if probe else True
        if result:
            return compiler, result
    return None, None


def compiler_version(compiler, env):
    try:
        _, output = run_cmd([compiler, "--version"], env=env, timeout=PROBE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "unknown version"
    for line in output.splitlines():
        if line.strip():
            return line.strip()
    return "unknown version"


def std_flag_options(kind):
    """Standard-flag lists to try in order."""
    stds = [C_STD] if kind == "c" else CXX_STD_CANDIDATES
    return [[std] for std in stds]


def detect_toolchain(kind, sanitize=False):
    """Select and probe the compiler and standard flags for kind; raise ToolError if unusable."""
    info = COMPILERS[kind]
    failures = []

    def probe(compiler):
        env = tool_env(compiler, sanitize)
        source, ext = (C_PROBE, ".c") if kind == "c" else (CPP_PROBE, ".cpp")
        for std_flags in std_flag_options(kind):
            ok, output = try_build(compiler, std_flags + WARN_FLAGS + ["-I", TOOLS_DIR], source, ext, env)
            if ok:
                return std_flags
            failures.append("%s %s:\n%s" % (compiler, " ".join(std_flags), output.strip()))
        return None

    compiler, std_flags = select_compiler(kind, os.environ, shutil.which, os.path.isfile, IS_WINDOWS, probe)
    if compiler is None:
        if failures:
            raise ToolError("no working %s compiler: every candidate failed a test compile; last errors:\n%s"
                            % (info["name"], "\n".join(indent_head(f, 15) for f in failures[-2:])))
        raise ToolError("no %s compiler found (looked for $%s, %s, %s and %s); see README section 9 "
                        "'MSYS2 CLANG64'" % (info["name"], info["env"], info["clang"],
                                             MSYS2_CLANG64_BIN, info["gcc"]))
    env = tool_env(compiler, sanitize)
    if sanitize:
        source, ext = (SANITIZE_PROBE_C, ".c") if kind == "c" else (SANITIZE_PROBE_CPP, ".cpp")
        ok, output = try_build(compiler, std_flags + WARN_FLAGS + SANITIZE_FLAGS, source, ext, env, run=True)
        if not ok:
            raise ToolError("sanitizers not supported by %s; see README 'MSYS2 CLANG64' setup\n%s"
                            % (compiler, indent_head(output, 15)))
    return Toolchain(kind, compiler, std_flags, compiler_version(compiler, env), env)


def discover(root):
    problems = []
    for lang in sorted(LANGS):
        lang_dir = os.path.join(root, lang)
        if not os.path.isdir(lang_dir):
            continue
        for topic in sorted(os.listdir(lang_dir)):
            topic_dir = os.path.join(lang_dir, topic)
            if not os.path.isdir(topic_dir):
                continue
            for name in sorted(os.listdir(topic_dir)):
                path = os.path.join(topic_dir, name)
                if os.path.isfile(os.path.join(path, LANGS[lang]["solution"])):
                    problems.append(Problem(lang, topic, name, path))
    return problems


def norm(path):
    return os.path.normcase(os.path.realpath(path))


def resolve_filter(path, root):
    """Resolve PATH (absolute, relative to the current directory or to the root)."""
    candidates = [path] if os.path.isabs(path) else [os.path.abspath(path), os.path.join(root, path)]
    for candidate in candidates:
        if os.path.exists(candidate):
            if os.path.isfile(candidate):
                candidate = os.path.dirname(candidate)
            return norm(candidate)
    return None


def select_problems(problems, paths, root):
    if not paths:
        return problems
    selected = []
    for path in paths:
        target = resolve_filter(path, root)
        matched = []
        if target is not None:
            prefix = target.rstrip("\\/") + os.sep
            matched = [p for p in problems if norm(p.path) == target or norm(p.path).startswith(prefix)]
        if not matched:
            raise ToolError("no problems under '%s'" % path)
        selected += [p for p in matched if p not in selected]
    return selected


def has_todo_marker(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return TODO_RE.search(f.read()) is not None
    except OSError:
        return False


def build_and_run(problem, toolchain, root, timeout, sanitize):
    """Return (status, detail, output to show) for one problem."""
    names = LANGS[problem.lang]
    test_src = os.path.join(problem.path, names["test"])
    if not os.path.isfile(test_src):
        return "NO TESTS", " (no %s)" % names["test"], ""
    out_dir = os.path.join(root, "build", *(["asan"] if sanitize else []),
                           problem.lang, problem.topic, problem.name)
    os.makedirs(out_dir, exist_ok=True)
    exe = os.path.join(out_dir, "test" + EXE)
    if os.path.exists(exe):
        try:
            os.remove(exe)
        except OSError:
            pass
    cmd = ([toolchain.path] + toolchain.std_flags + WARN_FLAGS + (SANITIZE_FLAGS if sanitize else [])
           + ["-I", TOOLS_DIR, test_src, "-o", exe])
    try:
        code, output = run_cmd(cmd, env=toolchain.env, cwd=problem.path, timeout=BUILD_TIMEOUT)
    except subprocess.TimeoutExpired:
        code, output = 1, "compiler timed out after %ds" % BUILD_TIMEOUT
    if code != 0:
        if has_todo_marker(os.path.join(problem.path, names["solution"])):
            return "TODO", " (solution not written yet; build errors below)", output
        return "BUILD FAIL", "", output
    try:
        code, output = run_cmd([exe], env=toolchain.env, cwd=problem.path, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", " (over %gs)" % timeout, ""
    if sanitize and any(marker in output for marker in SANITIZER_MARKERS):
        return "SANITIZER", "", output
    match = RESULT_RE.search(output)
    if match is None:
        return "TEST FAIL", " (exit code %d, no LC-RESULT line; did main return lc_finish()?)" % code, output
    checks, failed = int(match.group(1)), int(match.group(2))
    if code != 0 or failed:
        return "TEST FAIL", " (%d of %d checks failed, exit code %d)" % (failed, checks, code), output
    if checks == 0:
        return "NO TESTS", " (0 checks)", ""
    return "PASS", " (%d checks)" % checks, ""


def quiet_crash_dialogs():
    """Stop Windows from showing a crash dialog (which blocks until the timeout) when a test crashes."""
    if IS_WINDOWS:
        try:
            import ctypes
            ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
        except (ImportError, AttributeError, OSError):
            pass


def print_summary(counts):
    total = sum(counts.values())
    print("Summary: %d passed, %d no tests, %d todo, %d failed, %d total"
          % (counts["pass"], counts["no tests"], counts["todo"], counts["failed"], total))


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(
        description="Compile each problem's test.c / test.cpp into build/, run it and print a "
                    "pass/fail summary. Exit code 1 if a problem fails, 2 on usage/toolchain errors.",
        epilog="Statuses: PASS, NO TESTS, TODO, BUILD FAIL, TEST FAIL, TIMEOUT, SANITIZER. "
               "Compilers: $CC/$CXX, else clang, else MSYS2 CLANG64 (Windows), else gcc/g++.")
    parser.add_argument("paths", nargs="*", metavar="PATH",
                        help="problem, topic or language directory to build (default: all problems)")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="repository root (default: %(default)s)")
    parser.add_argument("--timeout", type=float, default=10.0, help="seconds per test run (default: 10)")
    parser.add_argument("--strict", action="store_true", help="also fail on TODO and NO TESTS")
    parser.add_argument("--sanitize", action="store_true",
                        help="build with " + " ".join(SANITIZE_FLAGS) + " (needs e.g. MSYS2 CLANG64)")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    counts = {"pass": 0, "no tests": 0, "todo": 0, "failed": 0}
    try:
        selected = select_problems(discover(root), args.paths, root)
    except ToolError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if not selected and not args.sanitize:
        print("No problems found under %s." % root)
        print_summary(counts)
        return 0

    quiet_crash_dialogs()
    kinds = sorted({p.lang for p in selected} | ({"c"} if args.sanitize else set()))
    toolchains = {}
    try:
        for kind in kinds:
            toolchains[kind] = detect_toolchain(kind, args.sanitize)
    except ToolError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    for kind in kinds:
        print(toolchains[kind].describe())
    print("Flags: %s%s" % (" ".join(WARN_FLAGS), " " + " ".join(SANITIZE_FLAGS) if args.sanitize else ""))
    print()

    for problem in selected:
        status, detail, output = build_and_run(problem, toolchains[problem.lang], root,
                                               args.timeout, args.sanitize)
        print("%-10s %s%s" % (status, problem.rel, detail))
        if output.strip():
            print(indent_head(output, 15 if status == "TODO" else 40))
        if status == "PASS":
            counts["pass"] += 1
        elif status == "NO TESTS":
            counts["no tests"] += 1
        elif status == "TODO":
            counts["todo"] += 1
        else:
            counts["failed"] += 1
        sys.stdout.flush()

    print()
    print_summary(counts)
    if counts["failed"] or (args.strict and (counts["no tests"] or counts["todo"])):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
