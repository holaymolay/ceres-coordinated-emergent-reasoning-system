# Stack Profile: C / C++

Use this profile for C/C++ projects (library or CLI). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Compiler toolchain per project (gcc/clang/msvc); CMake or Meson as common build systems.
- Lint/format: `clang-format`; static analysis via `clang-tidy`/`cppcheck`.
- Testing: `ctest` (CMake), `googletest`/`Catch2` frameworks.

## Project Layout
- `src/` for code; `include/` for headers; `tests/` for tests; `build/` ignored.
- Keep generated binaries/objects out of VCS.

## Development Commands
- `cmake -S . -B build` && `cmake --build build`
- `ctest --test-dir build` (after build) or framework-specific command.
- `clang-format -i` on touched files; `clang-tidy` per config.

## Style & Naming
- Follow project style guide; prefer RAII and smart pointers in C++.
- Avoid global mutable state; handle errors explicitly.

## Testing Guidance
- Keep unit tests small; mock external dependencies; gate integration tests appropriately.

## Configuration & Ops
- Use toolchain files or vcpkg/conan for deps if applicable; document required compilers/flags.
- Enable sanitizers (`-fsanitize=address,undefined`) in debug when feasible.
