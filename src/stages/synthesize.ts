import path from "path";
import { FILENAMES, DEFAULT_PDCA_PHASE } from "../constants";
import { loadConfig } from "../config";
import { ClarificationResponses, ValidationReport } from "../types";
import { validateIntentFile, validateResponses } from "../utils/validators";
import { fileExists, readJsonFile, readTextFile, readYamlFile, writeTextFile } from "../utils/fs";

export interface SynthesizeOptions {
  specId?: string;
}

function buildPrompt(
  specId: string,
  responses: ClarificationResponses,
  validationReport: ValidationReport,
  specPath: string,
  configPaths: { allowed: string[]; disallowed: string[] },
): string {
  const requirementIds = responses.requirements.map((req) => req.id);

  return `# Codex Execution Prompt

Spec ID: ${specId}
Concept: ${responses.metadata.concept_id}
PDCA Phase: ${responses.metadata.pdca_phase || DEFAULT_PDCA_PHASE}
Synchronizations: ${responses.metadata.synchronizations.join(", ")}

Source Artifacts
- ${FILENAMES.intentRaw}
- ${FILENAMES.clarificationResponses}
- ${specPath}
- ${FILENAMES.validationReport} (status: ${validationReport.status})

Allowed Paths
${configPaths.allowed.map((entry) => `- ${entry}`).join("\n")}

Disallowed Actions
${configPaths.disallowed.map((entry) => `- ${entry}`).join("\n")}

Required Outputs
- Tests and evidence covering requirements [${requirementIds.join(", ")}]
- Execution and validation logs referencing ${FILENAMES.validationReport}
- Updates to handover.md and completed.md reflecting work performed

Execution Rules
- Derived strictly from governed artifacts; no creative additions or LLM calls.
- Refuse to emit artifacts if any guardrail fails or validation status is not passed.
- Do not generate application code or bypass governance checkpoints.
`;
}

export async function runSynthesize(options: SynthesizeOptions): Promise<void> {
  if (!fileExists(FILENAMES.validationReport)) {
    throw new Error("Validation report missing. Run `spec-compile validate` first.");
  }

  const intent = validateIntentFile(await readYamlFile<unknown>(FILENAMES.intentRaw)).intent;
  const responses = validateResponses(await readYamlFile<unknown>(FILENAMES.clarificationResponses), intent);
  const specId = options.specId ?? responses.metadata.spec_id;
  if (!specId) {
    throw new Error("Spec ID is required for synthesis. Provide --spec-id or populate metadata.spec_id.");
  }
  if (responses.metadata.spec_id && responses.metadata.spec_id !== specId) {
    throw new Error(
      `Spec ID mismatch: responses metadata uses '${responses.metadata.spec_id}' but synthesis requested '${specId}'.`,
    );
  }

  const validationReport = await readJsonFile<ValidationReport>(FILENAMES.validationReport);
  if (validationReport.status !== "passed") {
    throw new Error("Cannot synthesize prompt while validation is failing. Resolve validation errors first.");
  }

  const specPath = path.join("specs", `${specId}.md`);
  if (!fileExists(specPath)) {
    throw new Error(`Spec not found at ${specPath}. Run normalization before synthesis.`);
  }

  // Ensure spec is readable; content itself is not mutated here.
  await readTextFile(specPath);

  const config = await loadConfig(".");
  const prompt = buildPrompt(specId, responses, validationReport, specPath, {
    allowed: config.allowed_paths,
    disallowed: config.disallowed_actions,
  });

  await writeTextFile(FILENAMES.synthesisPrompt, prompt);
  console.log(`Synthesis prompt written to ${FILENAMES.synthesisPrompt}`);
}
