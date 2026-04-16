import path from "path";
import { FILENAMES } from "./constants";
import { FrameworkConfig } from "./types";
import { fileExists, readYamlFile } from "./utils/fs";

const DEFAULT_CONFIG: FrameworkConfig = {
  concepts: [
    {
      id: "spec-generation-framework",
      name: "Spec Generation Framework",
      description: "Deterministic compiler that converts human intent into governed specifications.",
    },
  ],
  synchronizations: [
    { id: "governance-alignment", description: "Ensure outputs comply with governance contract." },
    { id: "run-records", description: "Persist deterministic run receipts for auditability." },
  ],
  security_defaults: [
    "Local filesystem only; no external service calls or secret material in artifacts.",
    "Deterministic execution; disable automatic retries or unstated fallbacks.",
    "No application-code generation; specifications only.",
  ],
  allowed_paths: ["src/**", "tests/**", "intent/**", "clarification/**", "specs/**", "validation/**", "synthesis/**"],
  disallowed_actions: [
    "Generate application code.",
    "Invoke LLMs inside the compiler pipeline.",
    "Bypass validation or governance gates.",
  ],
};

function ensureConfigDefaults(config: FrameworkConfig): FrameworkConfig {
  return {
    ...config,
    security_defaults: config.security_defaults ?? DEFAULT_CONFIG.security_defaults,
    allowed_paths: config.allowed_paths ?? DEFAULT_CONFIG.allowed_paths,
    disallowed_actions: config.disallowed_actions ?? DEFAULT_CONFIG.disallowed_actions,
  };
}

export async function loadConfig(baseDir = "."): Promise<FrameworkConfig> {
  const configPath = path.join(baseDir, FILENAMES.config);
  if (!fileExists(configPath)) {
    return DEFAULT_CONFIG;
  }

  const content = await readYamlFile<FrameworkConfig>(configPath);
  if (!content.concepts || content.concepts.length === 0) {
    throw new Error("Config must declare at least one concept.");
  }
  if (!content.synchronizations || content.synchronizations.length === 0) {
    throw new Error("Config must declare at least one synchronization.");
  }

  return ensureConfigDefaults(content);
}
