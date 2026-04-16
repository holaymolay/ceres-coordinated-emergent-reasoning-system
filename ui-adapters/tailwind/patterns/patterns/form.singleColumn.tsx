import React from "react";
import { UiIntent } from "../../../../skills/ui-intent-emit/src/types";
import { PatternRenderContext, TailwindPattern } from "../types";

export const formSingleColumn: TailwindPattern = {
  patternId: "form.singleColumn",
  match: (intent: UiIntent) => intent.type === "form.create",
  rank: () => 90,
  render: (intent: UiIntent, ctx: PatternRenderContext) => {
    const tokens = ctx.tokens;
    const layoutClass = tokens.layouts["single-column"] ?? "";

    return (
      <div className={tokens.components.container}>
        <div className={layoutClass}>
          {intent.content?.title ? <h2>{intent.content.title}</h2> : null}
          <div className={tokens.components.section}>
            {intent.components.fields.map((field) => (
              <div key={field.id} className={tokens.components.field.wrapper}>
                <label className={tokens.components.field.label}>{field.label}</label>
                <input className={tokens.components.field.control} type="text" />
                {field.helpText ? (
                  <span className={tokens.components.field.helper}>{field.helpText}</span>
                ) : null}
              </div>
            ))}
          </div>
          <div className={tokens.components.actionsRow}>
            {intent.components.actions.map((action) => (
              <button
                key={action.id}
                className={`${tokens.components.action.base} ${
                  tokens.components.action.emphasis.primary
                }`}
                type="button"
              >
                {action.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  },
};
