---
{"id":"plan-checks-must-be-literal-commands-d7abd42b","type":"lesson","status":"approved","scope":"project","sources":["run:run-962419a5-0fed-4976-a189-98194a0484de","neomind/flows/lc-new-problem","proposal:memory-a14f6ba7-894b-45a4-b2bf-9b6c27bff102","approval:approval-6cb141b6-a4e5-4f2e-b1b2-937c9b6cd048"],"tags":["flow-authoring","plan","checks"],"updatedAt":"2026-11-12T08:40:27.950Z","contentHash":"ef7f6e42cd93d5d3ef46fc360f14ef1abdbaf77c9c52f79c87cb39a3bac740c8"}
---
Plan checks must be literal commands with concrete paths: no placeholders like <topic> or <id4>_<slug>.
NeoMind runs each plan check as plain argv without a shell, so a check containing a placeholder (or '<' / '>') cannot run and the auto approval stops in waiting_approval. flow_validate does not catch this.
When the target path is only known at run time (e.g. a new problem directory), make the plan goal require the plan step to resolve it first and list the filled-in command, with a concrete example in the goal.