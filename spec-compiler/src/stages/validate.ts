import path from "path";
import { FILENAMES } from "../constants";
import { loadConfig } from "../config";
import { ValidationReport, ValidationRuleResult } from "../types";
import { collectMissingDecisions, validateIntentFile, validateResponses } from "../utils/validators";
import { fileExists, readTextFile, readYamlFile, writeJsonFile } from "../utils/fs";

export interface ValidateOptions {
  specId?: string;
}

function ruleResult(
  id: string,
  passed: boolean,
  message: string,
  counterexample?: string,
): ValidationRuleResult {
  return { id, passed, message, counterexample };
}

function detectPlaceholders(content: string): string | null {
  const tokens = ["TBD", "??", "<pending>", "REVISIT"];
  const hit = tokens.find((token) => content.includes(token));
  return hit || null;
}

export async function runValidate(options: ValidateOptions): Promise<void> {
  if (!fileExists(FILENAMES.intentRaw)) {
    throw new Error("intent/intent.raw.yaml is missing. Run `spec-compile intent` first.");
  }
  if (!fileExists(FILENAMES.clarificationResponses)) {
    throw new Error("clarification/responses.yaml is missing. Run `spec-compile clarify` first.");
  }

  const intent = validateIntentFile(await readYamlFile<unknown>(FILENAMES.intentRaw)).intent;
  const responses = validateResponses(await readYamlFile<unknown>(FILENAMES.clarificationResponses), intent);
  const specId = options.specId ?? responses.metadata.spec_id;
  if (!specId) {
    throw new Error("Spec ID is required for validation. Provide --spec-id or populate metadata.spec_id.");
  }
  if (responses.metadata.spec_id && responses.metadata.spec_id !== specId) {
    throw new Error(
      `Spec ID mismatch: responses metadata uses '${responses.metadata.spec_id}' but validation requested '${specId}'.`,
    );
  }

  const specPath = path.join("specs", `${specId}.md`);
  if (!fileExists(specPath)) {
    throw new Error(`Spec not found at ${specPath}. Run normalization first.`);
  }

  const config = await loadConfig(".");
  const specContent = await readTextFile(specPath);

  const rules: ValidationRuleResult[] = [];

  // Clarification completeness sanity check
  const unresolved = collectMissingDecisions(config, intent, responses);
  rules.push(
    ruleResult(
      "clarification-complete.rule",
      unresolved.length === 0,
      unresolved.length === 0
        ? "All clarification checks are resolved."
        : `${unresolved.length} clarification decision(s) remain unresolved.`,
      unresolved.length > 0 ? unresolved[0].issue : undefined,
    ),
  );

  // one-concept.rule
  const conceptIds = config.concepts.map((c) => c.id);
  const conceptValid = responses.metadata.concept_id.length > 0 && conceptIds.includes(responses.metadata.concept_id);
  rules.push(
    ruleResult(
      "one-concept.rule",
      conceptValid,
      conceptValid ? "Exactly one concept is referenced." : "Concept is missing or not in configured concepts.",
      conceptValid ? undefined : `concept_id=${responses.metadata.concept_id || "missing"}`,
    ),
  );

  // synchronization-required.rule
  const syncIds = config.synchronizations.map((s) => s.id);
  const syncValid =
    responses.metadata.synchronizations.length > 0 &&
    responses.metadata.synchronizations.every((sync) => syncIds.includes(sync));
  rules.push(
    ruleResult(
      "synchronization-required.rule",
      syncValid,
      syncValid ? "Synchronizations declared and valid." : "Synchronizations missing or invalid.",
      syncValid ? undefined : `synchronizations=${responses.metadata.synchronizations.join(", ") || "none"}`,
    ),
  );

  // data-ownership.rule
  const ownershipValid = responses.decisions.data_ownership.trim().length > 0;
  rules.push(
    ruleResult(
      "data-ownership.rule",
      ownershipValid,
      ownershipValid ? "Data ownership is explicitly defined." : "Data ownership is missing.",
      ownershipValid ? undefined : "responses.decisions.data_ownership is empty.",
    ),
  );

  // security-scope.rule
  const defaultsApplied = responses.security.defaults_applied === true;
  const defaultsPresent = config.security_defaults.every((entry) => specContent.includes(entry));
  const securityPassed = defaultsApplied && defaultsPresent;
  rules.push(
    ruleResult(
      "security-scope.rule",
      securityPassed,
      securityPassed
        ? "Security defaults are applied and present in the spec."
        : "Default security constraints are missing from responses or spec text.",
      securityPassed ? undefined : "Missing security defaults in spec content or responses.security.defaults_applied=false",
    ),
  );

  // requirement-to-test.traceability.rule
  const reqCoverage =
    responses.requirements.length > 0 &&
    responses.requirements.every(
      (req) => req.validation.tests.length > 0 && req.validation.acceptance_criteria.length > 0,
    );
  const uncovered = responses.requirements.find(
    (req) => req.validation.tests.length === 0 || req.validation.acceptance_criteria.length === 0,
  );
  rules.push(
    ruleResult(
      "requirement-to-test.traceability.rule",
      reqCoverage,
      reqCoverage
        ? "Every requirement has tests and acceptance criteria."
        : "Some requirements are missing tests or acceptance criteria.",
      uncovered
        ? `Requirement ${uncovered.id} lacks complete validation coverage.`
        : responses.requirements.length === 0
          ? "No requirements defined."
          : undefined,
    ),
  );

  // no-implicit-behavior.rule
  const implicitFlags =
    (responses.decisions.implicit_behaviors && responses.decisions.implicit_behaviors.length > 0) ||
    intent.unstated_assumptions.length > 0 ||
    intent.uncertainties.length > 0;
  const placeholderHit = detectPlaceholders(specContent);
  const implicitPassed = !implicitFlags && !placeholderHit;
  const implicitCounterexample = placeholderHit
    ? `Placeholder '${placeholderHit}' found in spec content.`
    : implicitFlags
      ? "Implicit behaviors, assumptions, or uncertainties remain."
      : undefined;
  rules.push(
    ruleResult(
      "no-implicit-behavior.rule",
      implicitPassed,
      implicitPassed ? "No implicit or placeholder behaviors remain." : "Implicit behavior or placeholders detected.",
      implicitCounterexample,
    ),
  );

  const errors = rules.filter((rule) => !rule.passed);
  const report: ValidationReport = {
    status: errors.length === 0 ? "passed" : "failed",
    generated_at: new Date().toISOString(),
    rules,
    errors,
  };

  await writeJsonFile(FILENAMES.validationReport, report);

  if (errors.length > 0) {
    console.error(`Validation failed. See ${FILENAMES.validationReport}`);
    process.exitCode = 1;
  } else {
    console.log(`Validation passed. Report written to ${FILENAMES.validationReport}`);
  }
}
