Yes. Below is a **single master Codex prompt** that is precise, enforceable, and aligned with your architecture. This is written to **add prompt-debugging as a first-class feature** at the **umbrella (ecosystem / hub) repo level**, without polluting governance or execution layers.

---

## MASTER CODEX PROMPT

**Feature: Prompt Debugging & Validation Layer (Pre-Execution)**

### Objective

Implement a **Prompt Debugging Layer** in the umbrella (hub) repository that intercepts **all user-originated prompts**—both file-based and chat-based—**before** they reach governance, orchestration, or execution layers.

This layer must:

* Validate intent
* Detect ambiguity or contradictions
* Enforce structural correctness
* Produce a debug report
* Block, refine, or approve prompts deterministically

---

### Scope (Hard Constraints)

* **This feature lives ONLY in the umbrella repository**
* Do **not** modify:

  * governance/orchestration repo internals
  * execution agents
* Governance remains enforcement-only, not interpretive
* Prompt debugging is **pre-governance**, not post-failure

---

### Prompt Intake Sources (Two Explicit Entry Points)

#### 1. File-Based Intake

* Source: `task-inbox.md`
* Flow:

  ```
  task-inbox.md
      → Prompt Debugger
      → todo.md (only if approved)
      → governance/orchestration
  ```

#### 2. Direct Chat Intake

* Source: interactive user prompts
* Flow:

  ```
  chat input
      → Prompt Debugger
      → execution routing (only if approved)
  ```

Both must use the **same debugging engine**.

---

### Core Feature: Prompt Debugger

Implement a **Prompt Debugger module** with the following responsibilities.

#### A. Prompt Classification

Determine:

* intent type (task, question, refactor, audit, exploration)
* target repo(s)
* destructive vs non-destructive
* execution required vs planning only

Reject if classification is ambiguous.

---

#### B. Structural Validation

Check for:

* missing subject
* unclear action
* unspecified scope
* implicit cross-repo side effects
* conflicting instructions
* undefined artifacts

Reject prompts that cannot be deterministically executed.

---

#### C. Governance Compatibility Check

Verify:

* single-concept rule (or require explicit synchronization)
* no bypass of enforcement
* no direct execution instructions to downstream agents

If violation detected → block with explanation.

---

#### D. Debug Output (Required Artifact)

Every prompt MUST yield a **Prompt Debug Report** before execution:

```yaml
prompt_id: <hash>
status: approved | needs-clarification | rejected
detected_intent: <string>
scope:
  repos: [umbrella, governance, ...]
  concepts: [...]
risk_level: low | medium | high
issues:
  - <explicit issue>
suggested_fix:
  - <rewrite suggestion>
decision_rationale: <concise explanation>
```

* If `approved`: forward prompt downstream
* If `needs-clarification`: return report to user
* If `rejected`: halt execution entirely

---

### Enforcement Rules (Non-Negotiable)

* **No prompt reaches governance without approval**
* **No silent auto-fixes**
* **No execution without a debug report**
* **Same prompt → same decision** (deterministic)

---

### Files / Modules to Create

In umbrella repo:

```
/prompt-debugger/
  ├─ classify.ts
  ├─ validate.ts
  ├─ risk-assess.ts
  ├─ debug-report.ts
  ├─ decision-engine.ts
  └─ README.md
```

Integration points:

* `task-inbox.md → debugger → todo.md`
* chat router → debugger → execution router

---

### Design Philosophy (Explicit)

* Prompt debugging is **spec validation for language**
* Treat prompts as **unsafe input**
* Assume ambiguity is failure
* Prefer rejection over misexecution
* Optimize for **explainability**, not permissiveness

---

### Success Criteria

* User can see *why* a prompt was blocked
* Governance layer receives only well-formed instructions
* Fewer downstream failures
* Reproducible prompt behavior
* Debugging happens **before** cost is incurred

---

### Deliverables

1. Prompt Debugger module implemented
2. Integration with both intake paths
3. README explaining:

   * why this exists
   * how prompts flow
   * how failures are handled
4. Example debug reports (approved + rejected)

---

### Final Instruction to Codex

> Implement this feature conservatively.
> Do not invent new execution semantics.
> Do not shortcut validation.
> This layer exists to prevent mistakes, not accelerate them.

---

If you want, next step can be **one of these only**:

1. Strip this down to a *minimal v0* (highest ROI, lowest surface area)
2. Convert this into a **formal Prompt Constitution**
3. Design the **debug report schema first** and work backward

Pick one.
