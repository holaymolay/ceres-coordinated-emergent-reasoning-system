import fs from "fs";
import { validateIntentOnly } from "./intent-validation";
import { validateCapability } from "./capability-validation";
import { validateConstitution } from "./constitution-validation";
import { GovernanceError } from "./types";

const readInput = (inputPath?: string): string => {
  if (!inputPath) {
    return fs.readFileSync(0, "utf-8");
  }
  return fs.readFileSync(inputPath, "utf-8");
};

const parseArgs = (args: string[]): { inputPath?: string; capability?: string } => {
  let inputPath: string | undefined;
  let capability: string | undefined;
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--capability" || arg === "-c") {
      capability = args[i + 1];
      i += 1;
      continue;
    }
    if (arg === "--input" || arg === "-i") {
      inputPath = args[i + 1];
      i += 1;
      continue;
    }
    if (arg.startsWith("-")) {
      throw new Error(`Unknown flag: ${arg}`);
    }
    if (!inputPath) {
      inputPath = arg;
      continue;
    }
    throw new Error(`Unexpected argument: ${arg}`);
  }
  return { inputPath, capability };
};

const emitResult = (ok: boolean, errors: GovernanceError[], capability?: string, pattern?: string) => {
  const payload = {
    ok,
    errors,
    capability,
    pattern,
  };
  process.stdout.write(JSON.stringify(payload));
};

// Entry point for CI: validates intent-only output and governance constraints.
try {
  const { inputPath, capability } = parseArgs(process.argv.slice(2));
  const raw = readInput(inputPath);
  const intentResult = validateIntentOnly(raw);
  const errors: GovernanceError[] = [...intentResult.errors];

  if (!intentResult.intent) {
    emitResult(false, errors);
    process.exit(1);
  }

  const capabilityResult = validateCapability(intentResult.intent, capability);
  errors.push(...capabilityResult.errors);

  if (capabilityResult.context) {
    errors.push(...validateConstitution(intentResult.intent, capabilityResult.context));
  }

  const ok = errors.length === 0;
  emitResult(ok, errors, capabilityResult.context?.capability, capabilityResult.context?.pattern);
  process.exit(ok ? 0 : 1);
} catch (error) {
  const message = error instanceof Error ? error.message : "Unknown error";
  emitResult(false, [{ code: "VALIDATOR_ERROR", message }]);
  process.exit(1);
}
