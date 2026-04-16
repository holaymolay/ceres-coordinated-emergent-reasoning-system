import React from "react";
import { UiIntent } from "../../../../skills/ui-intent-emit/src/types";
import { PatternRenderContext, TailwindPattern } from "../types";

export const tableStandard: TailwindPattern = {
  patternId: "table.standard",
  match: (intent: UiIntent) => intent.type === "table.create",
  rank: () => 90,
  render: (intent: UiIntent, ctx: PatternRenderContext) => {
    const tokens = ctx.tokens;
    const layoutClass = tokens.layouts["table-with-toolbar"] ?? "";

    return (
      <div className={tokens.components.container}>
        <div className={layoutClass}>
          {intent.content?.title ? <h2>{intent.content.title}</h2> : null}
          <div className={tokens.components.table.wrapper}>
            <table className={tokens.components.table.base}>
              <thead>
                <tr>
                  {intent.components.columns.map((column) => (
                    <th key={column.id} className={tokens.components.table.headerCell}>
                      {column.label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  {intent.components.columns.map((column) => (
                    <td key={column.id} className={tokens.components.table.bodyCell}>
                      —
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  },
};
