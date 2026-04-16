import path from "path";
import { FILENAMES, DEFAULT_PDCA_PHASE } from "../constants";
import { loadConfig } from "../config";
import { ClarificationResponses, ClarificationState, FrameworkConfig } from "../types";
import {
  collectMissingDecisions,
  validateIntentFile,
  validateResponses,
} from "../utils/validators";
import { fileExists, readYamlFile, writeTextFile } from "../utils/fs";

export interface NormalizeOptions {
  specId?: string;
}

function formatBullets(items: string[], indent = 0, fallback = "None recorded."): string {
  const prefix = `${" ".repeat(indent)}- `;
  if (!items || items.length === 0) {
    return `${prefix}${fallback}`;
  }
  return items.map((item) => `${prefix}${item}`).join("\n");
}

function buildSpecContent(specId: string, responses: ClarificationResponses, config: FrameworkConfig): string {
  const intent = responses.intent;
  const securityConstraints = Array.from(
    new Set([...config.security_defaults, ...responses.security.additional_constraints]),
  );

  const requirementsSection =
    responses.requirements.length === 0
      ? "- None recorded."
      : responses.requirements
          .map(
            (req) =>
              `- [${req.id}] ${req.description}${req.owner ? ` (Owner: ${req.owner})` : ""}`,
          )
          .join("\n");

  const testsSection =
    responses.requirements.length === 0
      ? "- None recorded."
      : responses.requirements
          .map((req) => {
            const tests = formatBullets(req.validation.tests, 2, "No tests recorded.");
            return `- [${req.id}] Tests:\n${tests}`;
          })
          .join("\n");

  const acceptanceSection =
    responses.requirements.length === 0
      ? "- None recorded."
      : responses.requirements
          .map((req) => {
            const acceptance = formatBullets(
              req.validation.acceptance_criteria,
              2,
              "No acceptance criteria recorded.",
            );
            return `- [${req.id}] Acceptance Criteria:\n${acceptance}`;
          })
          .join("\n");

  const traceabilitySection =
    responses.requirements.length === 0
      ? "- None recorded."
      : responses.requirements
          .map((req) => {
            const tests = req.validation.tests.length > 0 ? req.validation.tests.join("; ") : "No tests";
            const acceptance =
              req.validation.acceptance_criteria.length > 0
                ? req.validation.acceptance_criteria.join("; ")
                : "No acceptance criteria";
            return `- ${req.id}: Tests → ${tests}; Acceptance → ${acceptance}`;
          })
          .join("\n");

  return `# Spec: ${specId}

## Metadata
- Spec ID: ${specId}
- Concept: ${responses.metadata.concept_id}
- Synchronizations:
${formatBullets(responses.metadata.synchronizations, 2, "None declared.")}
- PDCA Phase: ${responses.metadata.pdca_phase || DEFAULT_PDCA_PHASE}
- Data Ownership: ${responses.decisions.data_ownership || "Unspecified"}

## Intent Summary
- User Goal: ${intent.user_goal}
- Context: ${intent.context}
- Stated Constraints:
${formatBullets(intent.stated_constraints, 2, "None recorded.")}
- Unstated Assumptions:
${formatBullets(intent.unstated_assumptions, 2, "None recorded (must be cleared before execution).")}
- Uncertainties:
${formatBullets(intent.uncertainties, 2, "None recorded (must be cleared before execution).")}
- Out of Scope:
${formatBullets(intent.out_of_scope, 2, "None recorded.")}

## Implicit Behaviors
${formatBullets(
  responses.decisions.implicit_behaviors || [],
  0,
  "None recorded (implicit behavior is not permitted).",
)}

## Requirements
${requirementsSection}

## Validation Plan
${testsSection}

## Acceptance Criteria
${acceptanceSection}

## Security Constraints
${formatBullets(securityConstraints, 0, "None recorded.")}

## Traceability
${traceabilitySection}
`;
}

function assertClarificationReady(state: ClarificationState): void {
  const openCount = state.questions?.length ?? 0;
  if (state.status !== "ready" || openCount > 0) {
    throw new Error(
      `Clarification is not ready (${openCount} blocking decision(s)). Resolve ${FILENAMES.clarificationQuestions} before normalization.`,
    );
  }
}

export async function runNormalize(options: NormalizeOptions): Promise<void> {
  if (!fileExists(FILENAMES.intentRaw)) {
    throw new Error("intent/intent.raw.yaml is missing. Run `spec-compile intent` first.");
  }
  if (!fileExists(FILENAMES.clarificationResponses) || !fileExists(FILENAMES.clarificationQuestions)) {
    throw new Error("Clarification artifacts are missing. Run `spec-compile clarify` before normalization.");
  }

  const config = await loadConfig(".");
  const intent = validateIntentFile(await readYamlFile<unknown>(FILENAMES.intentRaw)).intent;
  const responses = validateResponses(await readYamlFile<unknown>(FILENAMES.clarificationResponses), intent);
  const questionsState = await readYamlFile<ClarificationState>(FILENAMES.clarificationQuestions);
  assertClarificationReady(questionsState);

  const unresolved = collectMissingDecisions(config, intent, responses);
  if (unresolved.length > 0) {
    throw new Error(
      `Clarification gaps remain (${unresolved.length}). Rerun 'spec-compile clarify' after updating responses.`,
    );
  }

  const resolvedSpecId = options.specId ?? responses.metadata.spec_id;
  if (!resolvedSpecId) {
    throw new Error("Spec ID is required. Populate metadata.spec_id in clarification/responses.yaml.");
  }
  if (responses.metadata.spec_id && options.specId && options.specId !== responses.metadata.spec_id) {
    throw new Error(
      `Spec ID mismatch: responses metadata uses '${responses.metadata.spec_id}' but --spec-id is '${options.specId}'.`,
    );
  }

  const specContent = buildSpecContent(resolvedSpecId, responses, config);
  const targetPath = path.join("specs", `${resolvedSpecId}.md`);
  await writeTextFile(targetPath, specContent);
  console.log(`Normalized spec written to ${targetPath}`);
}
