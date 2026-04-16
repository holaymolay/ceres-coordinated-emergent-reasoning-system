import { FILENAMES, DEFAULT_PDCA_PHASE } from "../constants";
import { loadConfig } from "../config";
import { ClarificationResponses, ClarificationState, IntentRaw } from "../types";
import { fileExists, readYamlFile, writeYamlFile } from "../utils/fs";
import { collectMissingDecisions, validateIntentFile, validateResponses } from "../utils/validators";

export interface ClarifyOptions {
  force?: boolean;
}

function buildResponsesTemplate(intent: IntentRaw): ClarificationResponses {
  return {
    metadata: {
      spec_id: "",
      concept_id: "",
      synchronizations: [],
      pdca_phase: DEFAULT_PDCA_PHASE,
    },
    intent,
    decisions: {
      data_ownership: "",
      implicit_behaviors: [],
    },
    requirements: [],
    security: {
      defaults_applied: true,
      additional_constraints: [],
    },
  };
}

export async function runClarify(_options: ClarifyOptions): Promise<void> {
  if (!fileExists(FILENAMES.intentRaw)) {
    throw new Error("intent/intent.raw.yaml is missing. Run `spec-compile intent` first.");
  }

  const config = await loadConfig(".");
  const rawIntent = await readYamlFile<unknown>(FILENAMES.intentRaw);
  const intent = validateIntentFile(rawIntent).intent;

  let responses: ClarificationResponses;
  if (fileExists(FILENAMES.clarificationResponses)) {
    const existing = await readYamlFile<unknown>(FILENAMES.clarificationResponses);
    responses = validateResponses(existing, intent);
  } else {
    responses = buildResponsesTemplate(intent);
  }

  // Keep the intent section synchronized with the latest raw capture.
  responses.intent = intent;

  const questions = collectMissingDecisions(config, intent, responses);
  const state: ClarificationState = {
    status: questions.length === 0 ? "ready" : "pending",
    generated_at: new Date().toISOString(),
    questions,
    notes: [
      "Update clarification/responses.yaml to resolve blocking questions, then rerun `spec-compile clarify`.",
      "Questions are regenerated deterministically from rule checks; answers are captured in responses.yaml, not here.",
    ],
  };

  await writeYamlFile(FILENAMES.clarificationResponses, responses);
  await writeYamlFile(FILENAMES.clarificationQuestions, state);

  console.log(
    questions.length === 0
      ? "Clarification ready: no blocking questions."
      : `Clarification pending: ${questions.length} blocking decision(s) recorded in ${FILENAMES.clarificationQuestions}`,
  );
}
