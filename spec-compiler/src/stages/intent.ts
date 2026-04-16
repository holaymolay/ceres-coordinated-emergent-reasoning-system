import path from "path";
import { FILENAMES } from "../constants";
import { validateIntentFile } from "../utils/validators";
import { fileExists, readYamlFile, writeYamlFile } from "../utils/fs";

export interface IntentOptions {
  input?: string;
}

export async function runIntent(options: IntentOptions): Promise<void> {
  if (!options.input) {
    throw new Error("Intent capture requires --input <path> to a YAML file matching the intent schema.");
  }

  const sourcePath = path.resolve(options.input);
  if (!fileExists(sourcePath)) {
    throw new Error(`Input file not found: ${sourcePath}`);
  }

  const raw = await readYamlFile<unknown>(sourcePath);
  const intent = validateIntentFile(raw);

  await writeYamlFile(FILENAMES.intentRaw, intent);
  console.log(`Intent captured at ${FILENAMES.intentRaw}`);
}
