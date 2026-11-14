---
{"id":"codex-gpt-6-luna-writer-steps-2fc16949","type":"lesson","status":"approved","scope":"project","sources":["run-830882a2-e847-46d3-9de5-0045abc45ab0","run-c95e7d2e-8c65-4fa2-bb83-b5342674d8c2","neomind/skills/lc-theory-guide/SKILL.md","proposal:memory-a11184bc-c0d4-4fdb-88d8-faf227593a77","approval:approval-24f10234-0608-473a-9cd7-9dcb5c427409"],"tags":["flow-authoring","lc-theory","encoding"],"updatedAt":"2026-11-12T08:40:31.067Z","contentHash":"01b8fb20c1784c2015971d5848403cf229319761ce1b7017b57d8ed9df935c67"}
---
Codex (gpt-6-luna) writer steps on Windows save new Markdown files with a UTF-8 BOM; strip it after apply instead of instructing the agent.
- Symptom: both lc-theory runs produced theory.md starting with bytes EF BB BF; diacritics were intact and the auditor passed it.
- Do not add "write UTF-8 without BOM" to flow or profile text (it previously made an agent write the system code page and destroyed Vietnamese text). After neomind_apply, re-save the file as UTF-8 without BOM from the host side.
- Related: neomind_apply refuses when the checkout has an uncommitted or untracked file at a path the run changed; move or commit that file first.
- Writers also tend to render math as LaTeX stripped to bare parentheses, e.g. (10^5); require inline code such as `10^5` and `O(n log n)` in the skill and audit it.