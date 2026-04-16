# Stack Profile: Unity (C#)

Use this profile for Unity projects. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Unity version per project (check `ProjectVersion.txt`); align Editor/CI versions.
- Scripting: C#; package management via Unity Package Manager.
- Lint/format: follow C# style; use analyzers/Rider/VS tooling if configured.
- Testing: Unity Test Framework (EditMode/PlayMode).

## Project Layout
- Standard Unity structure with `Assets/`, `Packages/`, `ProjectSettings/`.
- Keep `Library/`, `Temp/`, `Logs/`, `obj/`, `build/` out of VCS.

## Development Commands
- Use Unity Editor/CLI for builds/tests.
- CLI examples: `unity -runTests -testPlatform editmode` (exact command depends on CI setup); build commands per project scripts.

## Style & Naming
- Follow C# conventions; use namespaces; avoid `Debug.Log` noise in committed code.
- Keep scripts focused; avoid heavy logic in MonoBehaviours when services suffice.

## Testing Guidance
- Write EditMode tests for logic; PlayMode tests for scene/interaction; mock external services.
- Keep tests deterministic; control randomness/time.

## Configuration & Ops
- Manage secrets/config outside repo; avoid committing license files/keys.
- Document required Unity version/CLI flags; keep build artifacts out of VCS.
