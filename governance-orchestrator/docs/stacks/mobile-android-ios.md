# Stack Profile: Mobile (Android / iOS)

Use this profile for native or cross-platform mobile apps (Android Studio/Xcode). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Android: Android Studio (latest stable), Kotlin preferred; Gradle wrapper (`./gradlew`) for builds.
- iOS: Xcode (project-specified version), Swift preferred; CocoaPods/SPM as per project.
- Cross-platform: follow project choice (React Native/Flutter) but keep native tooling aligned.

## Project Layout
- Android: `app/` module with `src/main/java|kotlin`, `src/androidTest`, `src/test`; Gradle config under `app/build.gradle[.kts]` and root `build.gradle[.kts]`.
- iOS: `.xcodeproj`/`.xcworkspace`; source under `<App>/`; tests under `<App>Tests`/`<App>UITests`.
- Keep build artifacts (`build/`, `DerivedData/`, `Pods/` when gitignored) out of VCS.

## Development Commands
- Android: `./gradlew assembleDebug` / `./gradlew test` / `./gradlew connectedAndroidTest` (emulator/device required).
- iOS: `xcodebuild test -scheme <Scheme> -destination 'platform=iOS Simulator,name=<Device>,OS=<Version>'` (adjust per project); `pod install` when using CocoaPods.
- Lint/format: Android `./gradlew lint ktlintFormat` (if configured); iOS `swiftlint`/`swiftformat` where configured.

## Style & Naming
- Follow Kotlin/Swift style guides; adhere to project lint rules (detekt/ktlint, SwiftLint).
- Keep modules small and feature-scoped; avoid leaking platform-specific code across layers.
- Use structured logging per platform; avoid stray `println`/`NSLog` in production.

## Testing Guidance
- Android: unit tests under `src/test`, instrumented tests under `src/androidTest`; prefer Robolectric for JVM-level UI where applicable.
- iOS: unit tests in `<App>Tests`, UI tests in `<App>UITests`; mock network/storage; avoid flaky simulator dependencies.
- For cross-platform stacks, align with framework testing tools (e.g., Jest/RTL for React Native, Flutter test/IntegrationTest).

## Configuration & Ops
- Keep secrets out of source; use Gradle properties, environment files, or platform keychains.
- Manage signing configs securely (keystores/provisioning profiles not in VCS).
- Cache dependencies with wrappers (`./gradlew`, `pod install`); pin toolchain versions in CI configs.
