# Enforcement Boundaries

## What Is a Hard Gate?
A hard gate is a deterministic block that prevents merge or release until a defined contract is satisfied.

## Allowed Hard Gates
- Schema/contract validity (configs, specs, artifacts).
- Safety and security checks that map to declared policies.
- Required artifact presence (e.g., run records, README/spec parity).
- CI validations that are deterministic and reproducible.

## Forbidden Hard Gates
- Subjective taste, style, or aesthetic preferences.
- Convenience-only checks (e.g., timing, non-deterministic heuristics).
- Runtime coupling to the umbrella repo; enforcement must stay inside each component repo.

## Boundary Principle
Enforcement is local to each component repository. Governance guidance is global but must not become a cross-repo runtime dependency.
