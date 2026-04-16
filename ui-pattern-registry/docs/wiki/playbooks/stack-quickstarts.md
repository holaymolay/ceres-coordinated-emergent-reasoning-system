# Playbook: Stack Quickstarts

Purpose: help agents pick and apply the right stack profile quickly. Always defer to the stack doc for details.

1) Identify the stack
- Match the repo/framework to a profile in `docs/stacks/`. If missing, clone `docs/stacks/STACK.template.md` and add it before proceeding.

2) Load required docs
- Core governance: `AGENTS.md`, `docs/agents.md`, `docs/humans/workflow-guide.md`.
- Stack profile: the relevant `docs/stacks/*.md`.
- Context/pruning: `docs/context-management.md`.

3) Development basics (per stack doc)
- Install deps with the stack’s package manager (npm/pip/go mod/dotnet/composer/etc.).
- Run lint/format/test commands from the profile before handing off results.
- Follow layout/logging/style rules in the profile; avoid ad-hoc tooling.

4) Configuration & secrets
- Use env files or platform config; never commit real secrets. Document new env keys in the stack doc/README.

5) Testing & coverage
- Place tests under the directories and naming conventions specified in the profile.
- Run the recommended test command; add coverage flags when provided.

6) Handover & logs
- Note which stack profile was used in `completed.md`/`handover.md` entries and changelog lines.

Stack catalog (see full docs in `docs/stacks/`):
- Angular (`angular.md`)
- Ansible (`ansible.md`)
- AWS Lambda (`aws-lambda.md`)
- Azure Functions (`azure-functions.md`)
- C/C++ (`c-cpp.md`)
- Cloudflare Workers (`cloudflare-workers.md`)
- Data/ML Python (`data-ml-python.md`)
- Django/DRF (`django-drf.md`)
- Deno/Fresh (`deno-fresh.md`)
- .NET/ASP.NET Core (`dotnet-aspnet.md`)
- Electron/Tauri (`electron-tauri.md`)
- Elixir/Phoenix (`elixir-phoenix.md`)
- FastAPI (`fastapi.md`)
- Flutter (`flutter.md`)
- Frontend React/TypeScript (`frontend-react.md`)
- GCP Cloud Functions/Run (`gcp-cloud-functions.md`)
- Go (`go.md`)
- Java/Spring (`java-spring.md`)
- Julia (`julia.md`)
- Kotlin JVM (`kotlin-jvm.md`)
- Mobile Android/iOS (`mobile-android-ios.md`)
- Next.js (`nextjs.md`)
- Node/Express (`node.md`)
- PHP/Laravel (`php-laravel.md`)
- PySpark/Databricks (`pyspark-databricks.md`)
- Python (`python.md`)
- React Native (`react-native.md`)
- Remix (`remix.md`)
- R/Tidyverse (`r-tidyverse.md`)
- Ruby on Rails (`ruby-rails.md`)
- Rust (`rust.md`)
- Scala/Play/Akka (`scala-play-akka.md`)
- SvelteKit (`sveltekit.md`)
- Terraform (`terraform.md`)
- Unity/C# (`unity.md`)
- Vue/Nuxt (`vue-nuxt.md`)
- WordPress (`wordpress.md`)
