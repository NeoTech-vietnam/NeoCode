#!/usr/bin/env python3
"""Create a practice problem directory: notes.md, a paste-ready solution file and a test file.

    python tools/new_problem.py <topic> <id> <slug> [--lang c|cpp] [--title T] [--fetch] [--root DIR]

The solution file only holds a TODO stub (or, with --fetch, the empty signature from
LeetCode); it never contains algorithm code. An existing problem directory is never
overwritten. --fetch is the only feature that uses the network; it reads LeetCode's
public GraphQL endpoint without logging in and falls back to the offline skeleton.
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.request

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(TOOLS_DIR)

# Keep in sync with the topic list in README.md section 9.
TOPICS = (
    "big-o", "array-string", "pointer", "hash", "two-pointers", "binary-search",
    "sliding-window", "linked-list", "stack-queue", "recursion", "tree", "heap",
    "graph", "sorting", "bit", "memory",
)

LANGS = {
    "c": {"solution": "solution.c", "test": "test.c"},
    "cpp": {"solution": "solution.cpp", "test": "test.cpp"},
}

# Headers that test.c / test.cpp include before the solution, mirroring what LeetCode
# provides implicitly. build_test.py compiles the same list to probe the C++ standard.
C_HEADERS = ("limits.h", "stdbool.h", "stdint.h", "stdio.h", "stdlib.h", "string.h")
CPP_HEADERS = (
    "algorithm", "climits", "cstdint", "cstdio", "cstdlib", "cstring", "functional",
    "iostream", "map", "queue", "set", "stack", "string", "unordered_map",
    "unordered_set", "utility", "vector",
)

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TODO_MARKER = "TODO: write your solution"

GRAPHQL_URL = "https://leetcode.com/graphql"
GRAPHQL_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    isPaidOnly
    codeSnippets { langSlug code }
    exampleTestcaseList
    metaData
    content
  }
}
"""
FETCH_TIMEOUT = 10


class FetchError(Exception):
    pass


def problem_url(slug):
    return "https://leetcode.com/problems/%s/" % slug


def title_from_slug(slug):
    return " ".join(word.capitalize() for word in slug.split("-"))


def fetch_question(slug):
    """POST the public GraphQL query (no login, no cookies) and return the decoded JSON."""
    url = os.environ.get("LC_GRAPHQL_URL") or GRAPHQL_URL
    body = json.dumps({
        "operationName": "questionData",
        "query": GRAPHQL_QUERY,
        "variables": {"titleSlug": slug},
    }).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (leetcode-practice tools/new_problem.py)",
        "Referer": problem_url(slug),
    })
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            raw = response.read()
    except Exception as e:  # any network, HTTP or URL error means "use the offline skeleton"
        raise FetchError("request to %s failed: %s" % (url, e))
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError as e:
        raise FetchError("invalid JSON response: %s" % e)


def parse_examples(question):
    """Return example strings like "a = 2, b = 3 -> 5" (expected output is best effort)."""
    try:
        meta = json.loads(question.get("metaData") or "{}")
        names = [param.get("name", "") for param in meta.get("params", [])]
    except (ValueError, AttributeError, TypeError):
        names = []
    text = html.unescape(re.sub(r"<[^>]+>", "", question.get("content") or ""))
    outputs = [output.strip() for output in re.findall(r"Output:\s*([^\n]*)", text)]
    examples = []
    for i, case in enumerate(question.get("exampleTestcaseList") or []):
        values = case.replace("\r\n", "\n").split("\n")
        if names and len(names) == len(values):
            example = ", ".join("%s = %s" % (name, value) for name, value in zip(names, values))
        else:
            example = ", ".join(values)
        if i < len(outputs) and outputs[i]:
            example += " -> " + outputs[i]
        examples.append(example)
    return examples


def parse_question(data, lang):
    """Extract id, title, the empty code snippet for lang and the examples from a GraphQL response."""
    question = None
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        question = data["data"].get("question")
    if not isinstance(question, dict):
        raise FetchError("problem not found in the response")
    if question.get("isPaidOnly"):
        raise FetchError("premium problem; the public API does not return its code")
    snippet = None
    for entry in question.get("codeSnippets") or []:
        if isinstance(entry, dict) and entry.get("langSlug") == lang:
            snippet = entry.get("code")
            break
    if not snippet:
        raise FetchError("no %s code snippet in the response" % lang)
    return {
        "id": str(question.get("questionFrontendId") or "").strip(),
        "title": str(question.get("title") or "").strip(),
        "snippet": snippet.replace("\r\n", "\n"),
        "examples": parse_examples(question),
    }


def add_todo_marker(code):
    """Put the TODO marker on the first blank line inside the first code block of a snippet."""
    lines = code.replace("\r\n", "\n").rstrip("\n").split("\n")
    seen_open = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if seen_open and not stripped:
            previous = lines[i - 1]
            indent = previous[:len(previous) - len(previous.lstrip())] + "    "
            lines[i] = indent + "// " + TODO_MARKER
            return "\n".join(lines) + "\n"
        if stripped.endswith("{") and not stripped.startswith(("*", "/*", "//")):
            seen_open = True
    return "// " + TODO_MARKER + "\n" + "\n".join(lines) + "\n"


def comment_safe(text):
    """Make text safe inside a // comment (no line continuation, no trigraphs)."""
    text = " ".join(text.split("\n")).replace("??", "? ?").rstrip()
    if text.endswith("\\"):
        text += " ."
    return text


def header_comment(pid, title, slug):
    return "// %d. %s\n// %s\n" % (pid, comment_safe(title), problem_url(slug))


def solution_file(lang, pid, title, slug, snippet):
    header = header_comment(pid, title, slug)
    if snippet is not None:
        return header + "\n" + add_todo_marker(snippet)
    if lang == "c":
        return header + (
            "// Paste-ready for LeetCode: keep only the LeetCode function here (no main, no tests).\n"
            "// TODO: replace the stub below with the C signature from LeetCode.\n"
            "\n"
            "int solution(void) {\n"
            "    // " + TODO_MARKER + "\n"
            "    return 0;\n"
            "}\n"
        )
    return header + (
        "// Paste-ready for LeetCode: keep only class Solution here (no main, no tests).\n"
        "\n"
        "class Solution {\n"
        "public:\n"
        "    // TODO: paste the LeetCode method signature and write your solution\n"
        "};\n"
    )


def test_file(lang, pid, title, examples):
    names = LANGS[lang]
    lines = ["// Local tests for %d. %s (not submitted to LeetCode)." % (pid, comment_safe(title))]
    lines += ["#include <%s>" % header for header in (C_HEADERS if lang == "c" else CPP_HEADERS)]
    lines.append("")
    if lang == "cpp":
        lines += ["using namespace std;", ""]
    lines += ['#include "lc.h"', '#include "%s"' % names["solution"], ""]
    if lang == "c":
        lines.append("int main(void) {")
        lines.append("    // TODO: add your own test cases, e.g. LC_CHECK(myFunction(...) == expected);")
    else:
        lines.append("int main() {")
        lines.append("    // TODO: add your own test cases, e.g. LC_CHECK(Solution().myMethod(...) == expected);")
    lines.append("    // Helpers in tools/lc.h: lc_list_from_array, lc_list_equals_array, lc_list_free,")
    lines.append("    // lc_tree_from_level (LC_NULL = missing node), lc_tree_free, lc_int_array_equals.")
    if examples:
        lines.append("    // Examples from LeetCode (input -> expected output):")
        lines += ["    //   " + comment_safe(example) for example in examples]
    lines.append("    return lc_finish();")
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_notes(template, pid, title, slug):
    return (template.replace("<Problem title>", title)
            .replace("<id>", str(pid))
            .replace("<slug>", slug))


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def error(message):
    print("error: " + message, file=sys.stderr)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(
        description="Create <lang>/<topic>/<id>_<slug>/ with notes.md, solution.* (paste-ready "
                    "TODO stub) and test.* (local test harness). Never overwrites a problem.",
        epilog="Topics (README section 9): " + ", ".join(TOPICS))
    parser.add_argument("topic", help="topic directory, one of the README section 9 topics")
    parser.add_argument("id", help="LeetCode problem number, e.g. 1")
    parser.add_argument("slug", help="LeetCode URL slug, e.g. two-sum")
    parser.add_argument("--lang", choices=sorted(LANGS), default="c", help="language (default: c)")
    parser.add_argument("--title", help="problem title (default: fetched title or derived from the slug)")
    parser.add_argument("--fetch", action="store_true",
                        help="read the title, empty code signature and examples from LeetCode's "
                             "public API (network, no login); falls back to the offline skeleton")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="repository root (default: %(default)s)")
    args = parser.parse_args(argv)

    if args.topic not in TOPICS:
        error("unknown topic '%s'; use one of: %s" % (args.topic, ", ".join(TOPICS)))
        return 2
    if not re.fullmatch(r"[0-9]+", args.id) or int(args.id) <= 0:
        error("problem id must be a positive integer, got '%s'" % args.id)
        return 2
    pid = int(args.id)
    if not SLUG_RE.match(args.slug):
        error("slug must look like 'two-sum' (lowercase letters, digits and dashes), got '%s'" % args.slug)
        return 2

    root = os.path.abspath(args.root)
    template_path = os.path.join(root, "templates", "notes.md")
    if not os.path.isfile(template_path):
        error("notes template not found: %s" % template_path)
        return 2
    target = os.path.join(root, args.lang, args.topic, "%04d_%s" % (pid, args.slug))
    rel_target = os.path.relpath(target, root).replace(os.sep, "/")
    if os.path.lexists(target):
        error("%s already exists; nothing was changed" % rel_target)
        return 1

    title = args.title
    snippet = None
    examples = []
    if args.fetch:
        try:
            question = parse_question(fetch_question(args.slug), args.lang)
        except (FetchError, AttributeError, TypeError, KeyError) as e:
            print("fetch failed: %s; using offline skeleton" % e)
        else:
            qid = question["id"]
            if not (qid.isdigit() and int(qid) == pid):
                error("LeetCode says '%s' is problem %s, not %d; nothing was written" % (args.slug, qid or "?", pid))
                return 2
            snippet = question["snippet"]
            examples = question["examples"]
            title = title or question["title"]
            print("fetched '%s' from LeetCode" % (question["title"] or args.slug))
    title = title or title_from_slug(args.slug)

    with open(template_path, encoding="utf-8") as f:
        template = f.read()
    names = LANGS[args.lang]
    os.makedirs(os.path.dirname(target), exist_ok=True)
    try:
        os.makedirs(target)
    except FileExistsError:
        error("%s already exists; nothing was changed" % rel_target)
        return 1
    write_text(os.path.join(target, "notes.md"), render_notes(template, pid, title, args.slug))
    write_text(os.path.join(target, names["solution"]), solution_file(args.lang, pid, title, args.slug, snippet))
    write_text(os.path.join(target, names["test"]), test_file(args.lang, pid, title, examples))

    print("Created %s/" % rel_target)
    print("  notes.md")
    print("  %-13s write your solution here, then paste it into LeetCode" % names["solution"])
    print("  %-13s add your LC_CHECK test cases here" % names["test"])
    print("Next: python tools/build_test.py %s" % rel_target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
