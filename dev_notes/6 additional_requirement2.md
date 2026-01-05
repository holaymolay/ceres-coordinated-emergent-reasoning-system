Here's another requirement I want to add. I think that the planning phase needs to result in a task list. So, I want that task list to be visible in the todo.md file. So, when we input, let's say, a lengthy requirement or a lengthy prompt, that gets converted into a series of tasks. I know the system probably does that already right now, but it's not visible to me as the human in my todo.md file, etc. And I can only really audit those changes after the fact in the completed .md file, but I kind of want to know what it's working on and what it plans to work on. And I'd like to be able to tweak and edit those, or at least have a conversation about them. But in order to do that, I need to have visibility into them.

This is a **good requirement** and it fits your architecture cleanly. It also fixes a real control blind spot.

You’re asking for **plan transparency + human-auditable intent**, not micromanagement.

Below is the correct way to add this without breaking determinism or turning todo.md into noise.

---

## Core principle (lock this in)

> **Planning must produce an explicit, inspectable execution graph, and `todo.md` is the human-readable projection of that graph.**

Right now the plan exists *implicitly* inside the agent. That’s unacceptable for a governed system.

---

## What must change (conceptually)

You already have:

* Objective
* Inference
* Planning
* Execution
* Completed.md

What’s missing is a **hard artifact boundary between Planning and Execution**.

That boundary is the **Task Plan**, and its projection is `todo.md`.

---

## New invariant rule (this is the key)

> **No code may be written until a task list has been generated, materialized in `todo.md`, and acknowledged.**

Acknowledged does *not* mean approved line-by-line.
It means:

* visible
* stable
* discussable

---

## How planning should work now (exactly)

### 1. Planning phase output = Task Plan (first-class artifact)

The planner must produce:

* a sequenced task list
* scoped tasks
* each task mapped to:

  * concept
  * phase
  * acceptance condition

This is **not prose**. This is structured intent.

---

### 2. Projection into `todo.md` (human-facing)

The system must then:

* write the tasks into `todo.md`
* using your existing formatting rules
* in execution order

Example:

```
- [ ] Define Objective Contract schema for inference phase
- [ ] Add Gap Ledger artifact template
- [ ] Register Inference stage in governance pipeline
- [ ] Implement Interrogator Agent (ADHD protocol enforced)
- [ ] Run shadow inference on sample objective
```

This is the **live execution queue**.

---

## Critical constraint (to avoid chaos)

### The system may NOT:

* add tasks ad hoc during execution
* silently reorder tasks
* skip tasks

### The system MAY:

* pause execution
* propose task edits
* split tasks
* reword tasks
* re-sequence tasks

…but only by **updating `todo.md` first**.

This keeps causality visible.

---

## How human interaction works (important)

You don’t want to edit `todo.md` directly every time.
You want **conversation-first, commit-second**.

So the flow is:

1. System writes initial `todo.md`

2. System asks (ADHD-friendly):

   > “Here is the proposed task plan.
   > Do you want to:
   >
   > 1. proceed
   > 2. modify tasks
   > 3. reorder tasks”

3. You respond in plain language

4. System applies edits to `todo.md`

5. Execution begins

This preserves authority without burden.

---

## During execution (visibility stays live)

As tasks run:

* completed tasks move to `completed.md`
* active task remains in `todo.md`
* future tasks stay visible

At any time, you can ask:

* “Why is this task here?”
* “Can we split this?”
* “Let’s defer this one”

Those become **plan revisions**, not interruptions.

---

## Relationship to your existing files (clean integration)

* `task-inbox.md`
  → raw intake, human-only

* `todo.md`
  → **planner output + execution queue**

* `completed.md`
  → immutable audit log

* `handover.md`
  → narrative summary

This aligns perfectly with what you already described in AGENTS.md.

---

## New hard rules to add to the framework

You should encode these verbatim (or close):

1. **Planning Phase Output Rule**
   Planning must emit a task list before any execution begins.

2. **Visibility Rule**
   The task list must be materialized in `todo.md`.

3. **Execution Gate Rule**
   No execution is permitted until the task list is visible and stable.

4. **Mutation Rule**
   Task changes require updating `todo.md` before execution continues.

5. **Audit Rule**
   Every completed task must be moved to `completed.md` before progressing.

These are enforceable. Codex can’t “forget” them.

---

## Why this does NOT slow you down

Counterintuitive but important:

* Writing tasks first **reduces rework**
* Visibility **reduces anxiety**
* You intervene *earlier*, not later
* Agents waste fewer cycles guessing intent

This aligns perfectly with your stated goal:

> minimize *your* subjective time, even if the machine works harder

---

## Net result (zoom out)

You now have:

* Inference → gaps
* Planning → tasks
* Execution → commits
* Verification → gates
* Visibility → `todo.md`

That completes the control loop.

---

## Next step (choose one)

We should now **update one artifact** to encode this:

1. Update **AI_BOOTSTRAP.md** to include task-visibility rules
2. Update **Planner Agent spec** to require `todo.md` emission
3. Write the **Codex bootstrap prompt** that installs all of this

Say the number.
