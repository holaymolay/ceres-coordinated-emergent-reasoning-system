# Stack Profile: Scala (Play / Akka)

Use this profile for Scala services using Play Framework or Akka. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- JDK 21; Scala version per build; build with sbt (preferred) or Gradle.
- Lint/format: `scalafmt`; lint with `scalafix`/`scapegoat` if configured.
- Testing: `sbt test`; frameworks: ScalaTest/specs2.

## Project Layout
- `app/` or `src/main/scala` for code; `test/` for tests; resources under `conf/` or `src/main/resources`.
- Build artifacts under `target/` (ignored).

## Development Commands
- `sbt compile`
- `sbt test`
- `sbt scalafmtAll` / `sbt scalafix` when configured
- `sbt run` (or `sbt ~run` for dev)

## Style & Naming
- Follow project scalafmt rules; prefer immutable data and explicit types.
- Use structured logging (e.g., `scala-logging`, `slf4j`); avoid printlns in production.

## Testing Guidance
- Keep tests deterministic; mock external services; isolate Akka actors with TestKit when applicable.
- For Play, use `WithApplication` or `GuiceOneAppPerSuite` patterns sparingly to keep tests fast.

## Configuration & Ops
- Config via `application.conf` (Typesafe Config); avoid hardcoded secrets.
- Pin plugin versions; run dependency/security checks (`sbt dependencyUpdates`, org-standard scanners).
