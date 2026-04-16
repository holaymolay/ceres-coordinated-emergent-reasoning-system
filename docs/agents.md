# Codex Agent Operational Framework

This document codifies how to deploy Codex-based agents for software delivery. By fusing PDCA continuous improvement, spec-driven development, and security controls, it ensures every automated contribution is traceable, reviewable, and production-ready.

## 1. Purpose
Define standardized execution workflows within the framework so that code generation remains consistent, secure, and verifiable across the stack.

## 2. Workflow Overview (PDCA Integration)
Each engagement cycles through Plan → Do → Check → Act, with explicit artifacts produced at every stage.

| Phase | Purpose | Artifacts |
|-------|----------|-----------|
| Plan  | Define task via Spec Document | specs/[task].md |
| Do    | Execute generation within defined constraints | generated code, logs |
| Check | Validate with tests, linting, security scans | ESLint, pytest, Bandit |
| Act   | Refine specs and update lessons learned | lessons_learned.md |

Use the repo wiki (`docs/wiki/index.md`) as the navigation layer for PDCA/spec context. It links to authoritative Concepts, Synchronizations, Specs, and Skills without replacing them.

## 3. Specification Template (Spec-Driven Model)
Every new task must anchor to an approved spec recorded under `specs/`. Use the following template; append Clarifications only when the Clarification Gate captures answers:

```markdown
Spec Title: <descriptive name>
Spec ID: <UUID or hash>
User Story: As a <role>, I need <capability> so that <outcome>.

Functional Requirements:
- <requirement 1>
- <requirement 2>

Non-functional Requirements:
- <performance, reliability, or compliance expectations>

Architecture Overview:
- <system boundaries, integrations, data flow diagram references>

Language & Framework Requirements:
- <required languages, frameworks, versions>

Testing Plan:
- <unit, integration, end-to-end strategies with tooling>

Dependencies:
- <libraries, services, feature toggles, migrations>

Input/Output Schemas:
- <API contracts, payload examples, schema references>

Clarifications (optional):
- Q: <question> A: <answer>

Validation Criteria:
- <measurable acceptance checks aligned with requirements>

Security Constraints:
- No external calls without approved connectors.
- Sanitize all inputs; validate outputs against schema before persistence.
```

### Skills and Specs
- Skills live in `/skills/` as deterministic tool packages (`skill.yaml` + schemas + implementation + tests); see `docs/skills/skill-library-v1.md`.
- Every Skill lists the governing spec ID, Concept manifest and Synchronization contracts (when applicable), validation plan, and security posture (see `docs/security.md` + `docs/access-manifest.md`).
- Before drafting a new spec, search the Skill library (and the wiki index) for reusable capabilities; if none exist, add a Skill immediately after the spec is approved.
- Skill changes follow the same review cadence as specs—update via PR, call out deltas in `handover.md`, and log decisions in `docs/wiki/design-decisions.md`.
- Reasoning Skills live under `skills/reasoning/` as manifest-only, non-executing constraints applied before planning; they are distinct from runtime Skills.

## 4. Execution Rules
- No free-form prompts: every task references its approved specification by ID.
- Before work begins, search `/skills/` and `docs/wiki/index.md` for an applicable Skill and record the Skill ID (or absence) in the plan, task list, and handover entry.
- Inject the Skill contract/usage notes (not prompts) next to the spec, Concept manifest, and Synchronization contracts in every agent prompt.
- Enforce single-responsibility: an agent handles one bounded task per run.
- Record spec ID/hash in all artifacts, commit messages, and handover notes for traceability.
- Execute code within the sanctioned sandbox; capture command logs and store them with the task record.
- Do not instruct humans to run framework scripts; the agent executes them as part of the framework run.
- Clarification Gate (pre-planner): When inputs are ambiguous or a reasoning check emits `needs_clarification`, ask targeted questions and record answers in the active spec under `Clarifications`.
  - Restart the run after updates; do not execute code or tools before clarification resolves.
- Reasoning Skills pipeline (pre-planner, post-clarification): Execute the ordered list in `skills/reasoning/pipeline.yaml` and abort on failures.
  - Emit structured logs (JSON) with fields: `event_type`, `skill_name`, `order`, `guarantees`, `violations`, `abort_reason`.
  - Planner receives only post-skill context and may not override reasoning guarantees.
  - Validate manifests with `scripts/validate-reasoning-skills.py` after edits or pipeline changes.
- Framework audit loop (speed + accuracy): For framework/governance changes, create a proposal and outcome entry in `docs/workflow-audit.md`.
  - The Improvement Gate question must be answered with the required statement before recommending or implementing a change.
  - Track speed (time-to-working result) and accuracy (first-pass success or fix-loop count).
- Adoption fast-path: When the user requests “apply this ai agents framework to my new project,” follow `docs/humans/workflow-adoption.md` and run `scripts/bootstrap-workflow.sh` to implement the framework in the target repo.
- Follow the operational handoffs (`handover.md`, `completed.md`) to document outcomes.
- Multi-attempt clarification: If the user pushes back twice on the same request (two failed attempts or “please fix” loops), stop implementing, restate the requirement in your own words, and ask clarifying questions until both sides align. Document the clarification in the plan/ledger before resuming work.
Operating modes:
- Continuous Mode (default): Work through all runnable items in `todo.md` in priority order, checking off tasks as they complete.
  - Decision Queue: Deferred decisions recorded as `Decision Needed: ...` under `## Decision Queue` in `todo.md`.
  - If a decision blocks downstream work, stop and request user input.
  - If a decision is non-blocking, add it to the Decision Queue and continue. Resolve the Decision Queue after the continuous run finishes.
  - Still obey all governance rules, including pre/post `todo-inbox.md` sweeps between tasks, PDCA steps, and security constraints.
- Iterative Mode (explicitly enabled): Work through the current task queue and pause for user input as soon as a decision is required to proceed.
  - Log activation in the planner ledger and `handover.md`; Iterative Mode ends when the declared scope ends or a blocker occurs.
- Continuous Execution Mode (phase-level override):
  - The human can explicitly enable a scoped “Continuous Execution Mode” to allow uninterrupted execution within a phase/task. Scope must be declared (e.g., “Phase 5 parity polish”).
  - Activation must be logged in the planner ledger and `handover.md`; it auto-expires at the end of the declared scope or on any blocker/failure.
  - Applies within either Iterative or Continuous Mode and only changes check-in cadence; all other constraints still apply.

## 4.1 Context Segmentation
- Every agent owns a ledger under `docs/context/<agent>.md` that captures only the context it needs (routing queues, pending specs, validation evidence).
- Ledger entries are grouped by Concept or feature; when switching domains, append a `Domain Shift` marker that summarizes the new focus and alerts the Pruning Agent.
- No agent should depend on another’s ledger directly—request context via the inter-agent protocol described in §4.3.

## 4.2 Pruning Workflow
1. The Planner identifies stale context (age > two tasks or domain change) and opens a pruning ticket in the Pruning Agent ledger.
2. The Pruning Agent summarizes the affected entries, proposed archive path (`docs/context/archive/<timestamp>-<agent>.md`), and rationale.
3. The user (or designated owner) approves or rejects the prune. Approval is required before any deletion.
4. Once approved, the Pruning Agent archives the entries, updates the originating ledger with a timestamp + link, and notes the action in `completed.md`/`handover.md`.
5. Rejected prunes remain in place but receive a `Prune Deferred` tag along with the user’s reason so future reviewers have context.

## 4.3 Inter-Agent Communication
- Agents exchange context via structured request/response blocks logged in their ledgers.
- **Request format:** `Context Request — <requesting agent> → <owning agent> — Concept/Spec: <id> — Need: <summary>`.
- **Response format:** mirror the request header with `Granted` or `Declined` plus the relevant excerpt or decline reason.
- The Pruning Agent monitors outstanding requests and can prompt owners when a response is overdue.
- Only share the minimal snippet needed; never copy entire ledgers between agents.

## 4.4 Framework Revision Snapshots
- After any change to AGENTS.md or framework-governing child docs (`docs/agents.md`, `docs/context-management.md`, wiki workflow pages, `docs/humans/workflow-guide.md`), copy the full set of framework files into local `ai_workflow_revisions/rev_n/` (gitignored by default).
- Number folders sequentially (`rev_001`, `rev_002`, …) and include the relative directory structure so reviewers can diff revisions easily.
- Record the revision ID and affected docs in `completed.md` and summarize the change in `handover.md`.
- Use `scripts/create-workflow-revision.sh` to generate archives; the script enforces folder numbering and copies every required file listed in `docs/workflow-revisions.md`.

## 4.5 Workflow Governance Todos
- `todo.md` reserves a `## Workflow Governance` section that sits between Bugs and Current Focus. Keep this section empty before returning to feature work.
- When the Router/Planner discover a workflow-change request (from `todo-inbox.md` or other sources), promote it directly into this section; do not bury it within feature tasks.
- The Planner documents the associated Concept/spec/skill (if any) plus ledger references for every governance todo so the audit trail stays complete.

## 4.6 Changelog Entries
- Every completed task must produce a timestamped entry in `CHANGELOG.md` capturing the task summary, relevant todos/specs, and contextual notes.
- Use ISO8601 timestamps and keep newest entries at the top for easy scanning.
- Reference the matching entry ID in `completed.md` and `handover.md` so reviewers can cross-check context quickly.

## 5. Validation Layer
- Run static analysis (ESLint for JS/TS, Ruff for Python) before presenting results.
- Maintain unit test coverage ≥ 80 % across touched modules; document deltas when exceptions apply.
- Execute integration tests relevant to the feature before requesting merge.
- Perform security scans (Bandit, npm-audit, dependency-review) and remediate findings or file risk waivers.

## 6. Review Protocol
1. Automated CI executes linting, testing, and security checks on the proposed changes.
2. Human review pairs the task owner with an independent reviewer to validate behavior, security posture, and documentation.
3. Results are logged in `lessons_learned.md` using the following schema:

```
Task ID: <UUID>
Outcome: pass|fail
Issues Found: <summary>
Adjustments: <spec/agent update>
Next Action: <who, when>
```

## 7. Reuse & Knowledge Base
- Store all validated specifications in `/specs/lib/` with immutable IDs.
- Tag each spec with domain labels (`scheduling`, `inspection`, `reporting`, `crm`, etc.) to accelerate discovery.
- Search the library for reusable assets before authoring a new spec; document reuse decisions in the Plan phase notes.

## 8. Continuous Improvement
- Review agent execution logs monthly to identify automation drift and efficiency opportunities.
- Update specification templates, validation tooling, and review checklists based on lessons learned.
- Archive deprecated specs with a rationale and link to replacement artifacts to preserve institutional knowledge.

## 9. Human Oversight
- AI aids delivery, but human approvers own the outcome; no automated merge is permitted.
- Every merge and production deployment requires signed approval from the designated owner and reviewer.
- Escalate deviations from spec or security posture to the Security Agent before proceeding.

## 10. Security & Compliance
- Never embed live credentials or secrets in specs, prompts, or generated artifacts; rely on `.env.sample` for configuration guidance.
- Log API and file-system access made by agents; retain logs per the retention policy in `docs/security.md`.
- Perform permission checks before executing privileged operations; abort when authorization is unclear.
- Align with the security playbook for dependency hygiene, incident response, and monitoring of automated changes.
