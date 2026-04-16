import { describe, expect, it } from "vitest";
import { UiEventSchema } from "../events.schema";
import { readFileSync } from "node:fs";
import { parse } from "yaml";

const validEvent = {
  id: "2b0df4a9-1df6-49ee-a7b0-638f0c7fb9b6",
  ts: "2025-12-24T18:00:00.000Z",
  uiSessionId: "session-123",
  intentId: "intent-form-create-001",
  type: "form.submitted",
  payload: { formId: "profile-create" },
  schemaVersion: "1.0.0",
  idempotencyKey: "profile-create:session-123:1",
};

describe("UiEventSchema", () => {
  it("accepts valid events", () => {
    const parsed = UiEventSchema.safeParse(validEvent);
    expect(parsed.success).toBe(true);
  });

  it("rejects missing idempotencyKey", () => {
    const invalid = { ...validEvent, idempotencyKey: "" };
    const parsed = UiEventSchema.safeParse(invalid);
    expect(parsed.success).toBe(false);
  });
});

describe("ui-event sync template", () => {
  it("contains required keys", () => {
    const contents = readFileSync(
      "synchronizations/templates/ui-event-sync.yaml",
      "utf-8"
    );
    const doc = parse(contents) as Record<string, unknown>;
    expect(doc.apiVersion).toBe("sync/v1");
    expect(doc.kind).toBe("Synchronization");
    expect(doc.trigger).toBeDefined();
    expect(doc.participants).toBeDefined();
    expect(doc.mapping).toBeDefined();
    expect(doc.constraints).toBeDefined();
  });
});
