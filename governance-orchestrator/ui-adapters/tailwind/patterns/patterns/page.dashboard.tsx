import React from "react";
import { UiIntent } from "../../../../skills/ui-intent-emit/src/types";
import { PatternRenderContext, TailwindPattern } from "../types";

export const pageDashboard: TailwindPattern = {
  patternId: "page.dashboard",
  match: (intent: UiIntent) => intent.type === "page.create",
  rank: () => 90,
  render: (intent: UiIntent, ctx: PatternRenderContext) => {
    const tokens = ctx.tokens;
    const layoutClass = tokens.layouts["two-column"] ?? "";

    return (
      <div className={tokens.components.container}>
        <div className={layoutClass}>
          {intent.sections.map((section) => (
            <section key={section.id} className={tokens.components.section}>
              {section.title ? <h3>{section.title}</h3> : null}
              {section.description ? <p>{section.description}</p> : null}
            </section>
          ))}
        </div>
      </div>
    );
  },
};
