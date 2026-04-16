import { DEFAULT_PDCA_PHASE } from "../constants";
import {
  ClarificationQuestion,
  ClarificationResponses,
  FrameworkConfig,
  IntentFile,
  IntentRaw,
  Requirement,
} from "../types";
import { isNonEmptyString, isStringArray } from "./fs";

function assertObject(value: unknown, message: string): asserts value is Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(message);
  }
}

function coerceString(value: unknown, field: string, allowEmpty = true): string {
  if (typeof value !== "string") {
    if (value === undefined && allowEmpty) {
      return "";
    }
    throw new Error(`${field} must be a string`);
  }
  if (!allowEmpty && value.trim() === "") {
    throw new Error(`${field} must be a non-empty string`);
  }
  return value;
}

function coerceStringArray(value: unknown, field: string): string[] {
  if (value === undefined) {
    return [];
  }
  if (!isStringArray(value)) {
    throw new Error(`${field} must be an array of strings`);
  }
  return value;
}

export function validateIntentFile(raw: unknown): IntentFile {
  assertObject(raw, "Intent file must be a YAML object with top-level 'intent'.");
  const intentNode = (raw as Record<string, unknown>).intent;
  assertObject(intentNode, "Intent file must include an 'intent' object.");

  const intent: IntentRaw = {
    user_goal: coerceString(intentNode.user_goal, "intent.user_goal", false),
    context: coerceString(intentNode.context, "intent.context", false),
    stated_constraints: coerceStringArray(intentNode.stated_constraints, "intent.stated_constraints"),
    unstated_assumptions: coerceStringArray(intentNode.unstated_assumptions, "intent.unstated_assumptions"),
    uncertainties: coerceStringArray(intentNode.uncertainties, "intent.uncertainties"),
    out_of_scope: coerceStringArray(intentNode.out_of_scope, "intent.out_of_scope"),
  };

  return { intent };
}

function coerceRequirement(raw: unknown, index: number): Requirement {
  assertObject(raw, `requirements[${index}] must be an object`);
  const validationNode = raw.validation ?? {};
  assertObject(validationNode, `requirements[${index}].validation must be an object`);
  const validation = {
    tests: coerceStringArray(validationNode.tests, `requirements[${index}].validation.tests`),
    acceptance_criteria: coerceStringArray(
      validationNode.acceptance_criteria,
      `requirements[${index}].validation.acceptance_criteria`,
    ),
  };

  return {
    id: coerceString(raw.id, `requirements[${index}].id`),
    description: coerceString(raw.description, `requirements[${index}].description`),
    owner: raw.owner && typeof raw.owner === "string" ? raw.owner : undefined,
    validation,
  };
}

export function validateResponses(raw: unknown, intent: IntentRaw): ClarificationResponses {
  assertObject(raw, "clarification/responses.yaml must be a YAML object");

  const metadataNode = raw.metadata ?? {};
  assertObject(metadataNode, "responses.metadata must be an object");
  const decisionsNode = raw.decisions ?? {};
  assertObject(decisionsNode, "responses.decisions must be an object");
  const securityNode = raw.security ?? {};
  assertObject(securityNode, "responses.security must be an object");

  const requirementsRaw = Array.isArray(raw.requirements) ? raw.requirements : [];
  const requirements = requirementsRaw.map((entry, index) => coerceRequirement(entry, index));

  const response: ClarificationResponses = {
    metadata: {
      spec_id: coerceString(metadataNode.spec_id, "responses.metadata.spec_id"),
      concept_id: coerceString(metadataNode.concept_id, "responses.metadata.concept_id"),
      synchronizations: coerceStringArray(metadataNode.synchronizations, "responses.metadata.synchronizations"),
      pdca_phase: coerceString(metadataNode.pdca_phase, "responses.metadata.pdca_phase") || DEFAULT_PDCA_PHASE,
    },
    intent,
    decisions: {
      data_ownership: coerceString(decisionsNode.data_ownership, "responses.decisions.data_ownership"),
      implicit_behaviors: coerceStringArray(decisionsNode.implicit_behaviors, "responses.decisions.implicit_behaviors"),
    },
    requirements,
    security: {
      defaults_applied:
        typeof securityNode.defaults_applied === "boolean" ? securityNode.defaults_applied : true,
      additional_constraints: coerceStringArray(
        securityNode.additional_constraints,
        "responses.security.additional_constraints",
      ),
    },
  };

  return response;
}

export function collectMissingDecisions(
  config: FrameworkConfig,
  intent: IntentRaw,
  responses: ClarificationResponses,
): ClarificationQuestion[] {
  const questions: ClarificationQuestion[] = [];

  const addQuestion = (id: string, prompt: string, options: string[], allowMultiple = false) => {
    questions.push({
      id,
      prompt,
      type: options.length === 2 && options.includes("yes") && options.includes("no") ? "binary" : "multiple-choice",
      options,
      allowMultiple,
      answer: null,
      blocking: true,
      issue: prompt,
    });
  };

  if (!isNonEmptyString(responses.metadata.spec_id)) {
    addQuestion("spec_id", "Set metadata.spec_id in clarification/responses.yaml", ["yes", "no"]);
  }

  const conceptIds = config.concepts.map((concept) => concept.id);
  if (!isNonEmptyString(responses.metadata.concept_id)) {
    addQuestion("concept_id", "Select exactly one Concept (metadata.concept_id)", conceptIds);
  } else if (!conceptIds.includes(responses.metadata.concept_id)) {
    addQuestion("concept_id_invalid", "Concept must be one of the configured concepts", conceptIds);
  }

  const syncIds = config.synchronizations.map((sync) => sync.id);
  if (!responses.metadata.synchronizations || responses.metadata.synchronizations.length === 0) {
    addQuestion("synchronizations", "Declare required synchronizations in metadata.synchronizations", syncIds, true);
  } else if (responses.metadata.synchronizations.some((sync) => !syncIds.includes(sync))) {
    addQuestion("synchronizations_invalid", "Synchronizations must match configured synchronizations", syncIds, true);
  }

  if (!isNonEmptyString(responses.decisions.data_ownership)) {
    addQuestion("data_ownership", "Define data ownership in decisions.data_ownership", ["yes", "no"]);
  }

  if (responses.requirements.length === 0) {
    addQuestion("requirements", "Add at least one requirement with validation coverage", ["yes", "no"]);
  } else {
    responses.requirements.forEach((requirement) => {
      if (!isNonEmptyString(requirement.id) || !isNonEmptyString(requirement.description)) {
        addQuestion(`requirement_${requirement.id || "missing"}`, "Each requirement needs id and description", [
          "yes",
          "no",
        ]);
      }
      if (!requirement.validation.tests || requirement.validation.tests.length === 0) {
        addQuestion(
          `tests_${requirement.id}`,
          `Requirement ${requirement.id} needs at least one validation test`,
          ["yes", "no"],
        );
      }
      if (!requirement.validation.acceptance_criteria || requirement.validation.acceptance_criteria.length === 0) {
        addQuestion(
          `acceptance_${requirement.id}`,
          `Requirement ${requirement.id} needs acceptance criteria`,
          ["yes", "no"],
        );
      }
    });
  }

  if (responses.security.defaults_applied !== true) {
    addQuestion("security_defaults", "Default security constraints must be applied", ["yes", "no"]);
  }

  if (responses.decisions.implicit_behaviors && responses.decisions.implicit_behaviors.length > 0) {
    addQuestion(
      "implicit_behaviors",
      "Resolve or document implicit behaviors so none remain unaddressed",
      ["yes", "no"],
    );
  }

  if (intent.unstated_assumptions.length > 0) {
    addQuestion(
      "unstated_assumptions",
      "Resolve unstated assumptions or convert them into explicit constraints",
      ["yes", "no"],
    );
  }

  if (intent.uncertainties.length > 0) {
    addQuestion(
      "uncertainties",
      "Resolve uncertainties before normalization (update intent or clarifications)",
      ["yes", "no"],
    );
  }

  return questions;
}
