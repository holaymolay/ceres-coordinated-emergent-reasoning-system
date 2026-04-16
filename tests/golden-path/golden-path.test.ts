import assert from "assert/strict";
import path from "path";
import { promises as fs } from "fs";
import { runRendererValidate } from "../../src/stages/renderer-validate";
import { runTaste } from "../../src/stages/taste";

async function readJson<T>(filePath: string): Promise<T> {
  const content = await fs.readFile(filePath, "utf8");
  return JSON.parse(content) as T;
}

async function writeRegistryFixture(registryPath: string): Promise<void> {
  const registry = {
    registry_version: "1.0.0",
    renderers: [
      {
        name: "golden-renderer",
        version: "0.1.0",
        target: "html",
        contract_id: "renderer-contract-v1",
      },
    ],
  };
  await fs.writeFile(registryPath, JSON.stringify(registry, null, 2), "utf8");
}

async function main(): Promise<void> {
  const fixturesDir = path.join(process.cwd(), "tests", "golden-path");
  const reportDir = path.join(fixturesDir, ".reports");
  await fs.mkdir(reportDir, { recursive: true });

  const manifestValidPath = path.join(fixturesDir, "renderer.valid.json");
  const manifestInvalidPath = path.join(fixturesDir, "renderer.invalid.json");
  const intentPath = path.join(fixturesDir, "intent.valid.json");
  const constitutionPath = path.join(process.cwd(), "config", "visual-constitution.json");
  const registryPath = path.join(reportDir, "renderer-registry.json");
  const rulesetPath = path.join(process.cwd(), "rules", "taste", "ruleset.json");

  await writeRegistryFixture(registryPath);

  // Valid pass: design intent + renderer manifest compile cleanly.
  const rendererReportPath = path.join(reportDir, "renderer-report.valid.json");
  await runRendererValidate({
    manifest: manifestValidPath,
    registry: registryPath,
    report: rendererReportPath,
  });
  const rendererReport = await readJson<{ status: string; errors: unknown[] }>(rendererReportPath);
  assert.equal(rendererReport.status, "passed", "Renderer manifest should validate against the contract and registry.");

  const tasteReportPath = path.join(reportDir, "taste-report.valid.json");
  await runTaste({
    manifest: manifestValidPath,
    constitution: constitutionPath,
    intent: intentPath,
    ruleset: rulesetPath,
    report: tasteReportPath,
    verbose: true,
  });
  const tasteReport = await readJson<{ status: string; errors: unknown[] }>(tasteReportPath);
  assert.equal(tasteReport.status, "passed", "Taste enforcement should pass for the valid manifest.");
  assert.equal(tasteReport.errors.length, 0, "Valid taste report should have no errors.");

  // Intentional violation: pattern used outside allowed intent should fail taste enforcement.
  const tasteReportFailPath = path.join(reportDir, "taste-report.invalid.json");
  await runTaste({
    manifest: manifestInvalidPath,
    constitution: constitutionPath,
    intent: intentPath,
    ruleset: rulesetPath,
    report: tasteReportFailPath,
    verbose: true,
    failFast: false,
  });
  const tasteFailReport = await readJson<{
    status: string;
    errors: { id: string; message: string; clause: string; intent_reference: string }[];
  }>(tasteReportFailPath);

  // Reset any exit codes set by failure-mode runners so the test process stays green after assertions.
  process.exitCode = 0;

  assert.equal(tasteFailReport.status, "failed", "Invalid manifest should fail taste enforcement.");
  const patternError = tasteFailReport.errors.find((rule) => rule.id === "patterns.intent.rule");
  assert.ok(patternError, "Expected patterns.intent.rule to surface the violation.");
  assert.equal(patternError!.id, "patterns.intent.rule", "Rule identifier should be surfaced with the violation.");
  assert.ok(
    /intent/i.test(patternError!.message),
    "Failure message should attribute the violation to design intent/pattern governance.",
  );
  assert.ok(
    /pattern/i.test(patternError!.message) || /constitution/i.test(patternError!.message),
    "Failure message should cite the pattern or constitution source that was violated.",
  );
  assert.ok(
    /design_intent|intent/i.test(patternError!.intent_reference),
    "Intent reference should attribute the failure to design intent constraints.",
  );

  console.log("Golden path integration test passed.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
