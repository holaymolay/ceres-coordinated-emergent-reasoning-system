import { describe, expect, it } from "vitest";
import { selectPattern } from "../selectPattern";
import { tailwindPatterns } from "../registry";
import { TailwindPattern } from "../types";

const formIntent = {
  id: "intent-form-create-001",
  type: "form.create",
  schemaVersion: "1.0.0",
  purpose: { summary: "Collect data" },
  components: { fields: [], columns: [], actions: [] },
} as const;

describe("selectPattern", () => {
  it("selects the highest rank match", () => {
    const selected = selectPattern(formIntent, tailwindPatterns);
    expect(selected?.patternId).toBe("form.singleColumn");
  });

  it("breaks ties by patternId", () => {
    const a: TailwindPattern = {
      patternId: "alpha",
      match: () => true,
      rank: () => 10,
      render: () => null as unknown as JSX.Element,
    };
    const b: TailwindPattern = {
      patternId: "beta",
      match: () => true,
      rank: () => 10,
      render: () => null as unknown as JSX.Element,
    };
    const selected = selectPattern(formIntent, [b, a]);
    expect(selected?.patternId).toBe("alpha");
  });
});
