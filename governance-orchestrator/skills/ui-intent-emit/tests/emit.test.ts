import { describe, expect, it } from "vitest";
import { emitUiIntent, validateUiIntent } from "../src/emit";

const validForm = {
  id: "intent-form-create-001",
  type: "form.create",
  schemaVersion: "1.0.0",
  purpose: { summary: "Collect basic profile information" },
  formId: "profile-create",
  components: {
    fields: [{ id: "first_name", label: "First name", kind: "text" }],
    columns: [],
    actions: [{ id: "submit", label: "Create profile", intent: "submit" }],
  },
};

describe("emitUiIntent", () => {
  it("returns a validated intent", () => {
    const result = emitUiIntent(validForm);
    expect(result.type).toBe("form.create");
  });

  it("rejects missing formId", () => {
    const invalid = { ...validForm, formId: undefined };
    const outcome = validateUiIntent(invalid);
    expect(outcome.success).toBe(false);
  });
});
