import fs from "fs";
import path from "path";
import { promisify } from "util";
import yaml from "js-yaml";

const mkdir = promisify(fs.mkdir);
const writeFile = promisify(fs.writeFile);
const readFile = promisify(fs.readFile);

export async function ensureDir(targetPath: string): Promise<void> {
  await mkdir(targetPath, { recursive: true });
}

export async function writeYamlFile(filePath: string, data: unknown): Promise<void> {
  const dir = path.dirname(filePath);
  await ensureDir(dir);
  const content = yaml.dump(data, { noRefs: true, lineWidth: 120 });
  await writeFile(filePath, content, "utf8");
}

export async function readYamlFile<T>(filePath: string): Promise<T> {
  const content = await readFile(filePath, "utf8");
  return yaml.load(content) as T;
}

export async function writeJsonFile(filePath: string, data: unknown): Promise<void> {
  const dir = path.dirname(filePath);
  await ensureDir(dir);
  const content = JSON.stringify(data, null, 2);
  await writeFile(filePath, content, "utf8");
}

export async function readJsonFile<T>(filePath: string): Promise<T> {
  const content = await readFile(filePath, "utf8");
  return JSON.parse(content) as T;
}

export async function writeTextFile(filePath: string, data: string): Promise<void> {
  const dir = path.dirname(filePath);
  await ensureDir(dir);
  await writeFile(filePath, data, "utf8");
}

export async function readTextFile(filePath: string): Promise<string> {
  return readFile(filePath, "utf8");
}

export function fileExists(filePath: string): boolean {
  return fs.existsSync(filePath);
}

export function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

export function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((entry) => typeof entry === "string");
}
