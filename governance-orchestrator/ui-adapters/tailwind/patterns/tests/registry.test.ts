import { describe, expect, it } from "vitest";
import { tailwindPatterns } from "../registry";

describe("pattern registry", () => {
  it("registers required patterns", () => {
    const ids = tailwindPatterns.map((pattern) => pattern.patternId);
    expect(ids).toContain("form.singleColumn");
    expect(ids).toContain("form.twoColumn");
    expect(ids).toContain("table.standard");
    expect(ids).toContain("page.dashboard");
  });
});
