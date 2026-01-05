I'd like to add an additional requirement. I would like the questions and the back and forth communication between the llm and the human to be ADHD friendly. I think that would be the lowest common denominator and even neurotypical people will have an easy time with that communication style and approach, correct me if I'm wrong, but I think that is true

You’re **not wrong**. Designing the interaction to be ADHD-friendly is a strict improvement, not a tradeoff. It lowers cognitive load for everyone and **reduces error rates**, especially in agentic back-and-forth.

What matters is that this is **not a tone choice**. It’s a **control and interface constraint**.

Below is how to formalize it so it’s enforceable by agents, not vibes.

---

## Why ADHD-friendly is the correct lowest common denominator

From a systems perspective:

* ADHD failure modes = **working memory overload**, **context loss**, **decision fatigue**
* LLM failure modes = **hallucination**, **scope drift**, **assumption stacking**

These failure modes **overlap**.

So designing for ADHD:

* reduces branching
* reduces ambiguity
* forces explicit state
* forces atomic decisions

That directly improves determinism.

Neurotypical users don’t lose anything because:

* short, structured prompts are faster to parse
* single decisions are easier than multi-part ones
* explicit state beats implicit context for everyone

This is the same reason good APIs feel “boring”.

---

## Make “ADHD-friendly” a formal protocol, not a preference

You do **not** want:

> “Be concise and friendly”

You want **hard rules**.

### Rule 1: One decision per turn (non-negotiable)

* One question
* One gap
* One decision

Never:

* multi-part questions
* “while we’re at it”
* stacked hypotheticals

This is already aligned with your stated preference.

---

### Rule 2: Questions must be *binary or bounded*

Allowed:

* Yes / No
* Pick 1 of N (≤5)
* Short fill-in with example

Disallowed:

* “What do you think about…”
* “Can you describe…”
* “How would you like…”

If free-form input is required, the system must:

* explain *why*
* provide a concrete example template

---

### Rule 3: Always show *why* the question exists (one line)

Every question must include:

> **Why this matters:** <one sentence tied to execution or risk>

This prevents the user from context-switching mentally to “why am I being asked this”.

---

### Rule 4: State is always visible and summarized

Before asking a question, the system must show:

* What is already decided
* What is undecided (the current gap)
* What will happen after this answer

But **compressed**:

Example:

```
Status:
✓ Core goal defined
✓ Constraints known
✗ Acceptance criteria unclear

Question (Gap G-003):
Do you want X or Y?

Why this matters:
This determines the validation strategy and test scope.
```

No narrative. No recap essay.

---

### Rule 5: Progressive disclosure only

The system is forbidden from:

* explaining future steps
* previewing downstream complexity
* “just so you know” statements

The user only sees:

* the current gap
* the immediate consequence

This keeps attention anchored.

---

### Rule 6: Explicit pause points

After an answer:

* system **acknowledges in one line**
* updates artifacts
* then **stops**

No automatic follow-up question unless explicitly allowed by policy.

This prevents conversational runaway.

---

## Where this lives architecturally

This is **not** a UI concern.

It belongs in:

* **Inference policy**
* **Interrogator Agent rules**
* **Conversation contract**

Concretely:

* The Interrogator Agent **cannot ask a question** unless it conforms to the ADHD protocol
* Violations are rejected the same way a schema violation would be

---

## How this integrates with your earlier design

* Gap Ledger → source of truth
* One gap → one question
* Question format enforced
* Answer → structured delta
* Delta updates Objective / Plan
* Loop continues

This keeps inference clean, human-friendly, and machine-verifiable.

---

## Important reframing (this is subtle but critical)

You are not making the system “ADHD-friendly”.

You are making it:

> **Attention-bounded, state-explicit, and decision-atomic**

ADHD friendliness is a *side effect* of good control design.

---

## Updated requirement (clean, formal wording)

You can safely add this to the framework:

> **All human–LLM interactions must follow an attention-bounded protocol: one decision per turn, bounded questions, explicit rationale, visible state, and progressive disclosure. This protocol applies universally to inference, planning, and execution phases.**

That’s enforceable.

---

If you want next, I can:

* encode this as **Interrogator Agent constraints**
* or bake it directly into **AI_BOOTSTRAP.md**
* or reflect it into the **Codex bootstrap prompt**

Say which artifact to update first.
