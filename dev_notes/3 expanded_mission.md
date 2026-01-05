This project enforces agentic problem-solving as a governed, closed-loop control system. It produces deterministic, evolvable outcomes by constraining AI behavior through formal artifacts, staged execution, synchronization contracts, and continuous verification—without LLM error loops. How do we make the project expand into a more automated inference machine that can ask and/or answer questions to fill in the gaps of a given objective?

Make it a first-class subsystem: **Objective → Gaps → Queries → Evidence → Commitments**.

### 1) Add an explicit “Inference Loop” stage to your control plane

Right now you have: *formal artifacts + staged execution + verification*.

Add one more invariant stage before “Plan” (or inside Plan):

**Infer**

* Detect missing info required to proceed safely
* Decide whether to **ask** (human query) or **answer** (self-retrieval / computation / tool call)
* Produce *bounded* updates to artifacts (not free-form text)

This turns the system from “governed execution” into a **governed inference machine**.

---

### 2) Represent “gaps” as a typed artifact, not chat

Create an artifact class like:

**Objective Contract**

* goal
* success criteria
* constraints
* context sources allowed
* risk profile

**Gap Ledger**
Each gap is a record with:

* `gap_id`
* `type`: definition | constraint | dependency | acceptance | risk | data | interface | scope
* `blocking`: yes/no
* `answerable_by_system`: yes/no (based on allowed sources/tools)
* `resolution_method`: ask_user | search_repo | run_tests | inspect_code | web | derive
* `confidence_required`: low/med/high
* `status`: open/resolved/deferred
* `evidence_links`: pointers to files/lines/commands/results

The ledger becomes the machine’s *work queue*.

---

### 3) Add two new agents (or roles) with hard boundaries

**Inference Agent**

* Reads Objective Contract + current artifacts
* Produces Gap Ledger entries
* Proposes resolution plan for each gap

**Interrogator Agent**

* Generates user questions *only from Gap Ledger*
* One question per turn (your preference)
* Must explain why it’s blocking in one line
* Never asks “nice-to-have” questions when blockers exist

Optional but powerful:

**Resolver Agent**

* Answers “answerable_by_system” gaps via:

  * repo search
  * static analysis
  * running tests
  * schema inspection
  * limited web (if allowed)
* Must attach evidence to ledger

---

### 4) Enforce “commitments” to prevent hallucinated gap-filling

The danger is the system inventing answers to move forward.

Add a rule:

A gap can be marked **resolved** only if it has:

* **Evidence** (file/line, command output, test result, citation), or
* **User-provided answer** (captured verbatim), or
* **Explicit assumption** with:

  * risk rating
  * fallback plan
  * expiration (must be revisited)

This preserves determinism.

---

### 5) Turn questions into structured deltas, not prose

When the user answers a question, the system must convert it into:

* spec fields
* constraints
* schema updates
* synchronization clauses
* acceptance criteria

That is how you “fill gaps” without drifting.

---

### 6) Automation policy: when to ask vs when to infer

Define a simple decision policy (you can encode it):

Ask the user when:

* it’s a preference/aesthetic/product decision
* it changes scope/cost materially
* it’s a business rule
* confidence would otherwise be < required threshold

Infer automatically when:

* the answer exists in repo/docs/logs
* it can be derived (math, type inference, schema inference)
* it can be validated cheaply (tests/lint/schema check)

This gives you the “more automated” behavior without chaos.

---

### 7) What this looks like in practice (flow)

1. User provides objective
2. System builds Objective Contract
3. Inference Agent emits Gap Ledger
4. Resolver Agent auto-resolves what it can (with evidence)
5. Interrogator asks remaining **blocking** gaps (one at a time)
6. Once blockers cleared → normal PDCA execution proceeds
7. Verification stage can reopen gaps if tests fail (closed-loop)

---

### 8) Where this should live in your ecosystem

You already have the right separation:

* Governance/orchestration repo enforces stages + rules
* Spec compiler repo can generate Objective Contract + Gap Ledger templates
* UI/registry repos can provide structured inputs and schema constraints

So the “Inference Machine” is not a new product—it's a **new mandatory stage + new artifacts + new roles**.

---

