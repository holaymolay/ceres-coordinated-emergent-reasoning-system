# AI Framework User Guide (Cheat Sheet)

Use this one-pager to get fast, accurate results with minimal iteration.

The framework is AI-operated: use chat or `todo-inbox.md`; the agent runs scripts and updates AI-managed files.

## Quick Apply Phrase
“Apply this ai agents framework to my new project at <path> using <stack> (with or without Skills).”

## 1) Use the Request Pack
```markdown
Goal:
Context:
Constraints:
Success criteria:
Testing:
```
Use `docs/humans/glossary.md` if any term is unclear.

## 2) Keep Scope Tight
- One feature/behavior per request.
- Avoid mixing refactors with new behavior.
- If large, ask for a plan first.

## 3) Answer Clarifications Fast
When asked, reply with concrete choices (stack, data store, APIs, constraints).

## 4) Provide Tests
Give a test command or a clear manual verification step.

## 5) Avoid These
- Vague goals (“make it better”).
- Mixed priorities (“refactor + add + investigate”).
- Missing constraints (stack, versions, security, non-goals).

## 6) Use Modes Wisely
- Continuous Mode = speed (default).
- Iterative Mode = more control (stops on first decision).

## 7) Know the Metrics
- Speed = time to working result.
- Accuracy = fix-loop count, first-pass success.
