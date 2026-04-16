import React from "react";
import {
  AlertShowIntent,
  CtaRequestIntent,
  FormCreateIntent,
  ModalOpenIntent,
  PageCreateIntent,
  TableCreateIntent,
  UiAction,
  UiField,
  UiIntent,
  ValidatedUiIntent,
} from "../intent/intent-schema";
import { TailwindAdapter } from "./adapter-contract";
import { layoutPatterns, resolvePattern } from "./patterns";
import { tailwindTokens } from "./tokens";
import { selectPattern } from "../../../../ui-adapters/tailwind/patterns/selectPattern";
import { tailwindPatterns } from "../../../../ui-adapters/tailwind/patterns/registry";

// Adapter boundary: JSX and Tailwind tokens are confined to this file and tokens.ts.

const resolveActionEmphasis = (action: UiAction): "primary" | "secondary" | "danger" => {
  if (action.intent === "confirm") {
    return "danger";
  }
  if (action.intent === "cancel" || action.intent === "dismiss") {
    return "secondary";
  }
  return "primary";
};

const renderFieldControl = (field: UiField): React.ReactElement => {
  const baseProps = {
    id: field.id,
    name: field.id,
    className: tailwindTokens.components.field.control,
  };

  switch (field.kind) {
    case "select":
      return (
        <select {...baseProps}>
          {(field.options ?? []).map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      );
    case "textarea":
      return <textarea {...baseProps} rows={4} />;
    case "checkbox":
      return <input {...baseProps} type="checkbox" />;
    case "number":
      return <input {...baseProps} type="number" placeholder={field.placeholder} />;
    case "date":
      return <input {...baseProps} type="date" />;
    case "text":
    default:
      return <input {...baseProps} type="text" placeholder={field.placeholder} />;
  }
};

const renderField = (field: UiField): React.ReactElement => (
  <div key={field.id} className={tailwindTokens.components.field.wrapper}>
    <label htmlFor={field.id} className={tailwindTokens.components.field.label}>
      {field.label}
    </label>
    {renderFieldControl(field)}
    {field.helpText ? (
      <span className={tailwindTokens.components.field.helper}>{field.helpText}</span>
    ) : null}
  </div>
);

const renderAction = (action: UiAction): React.ReactElement => {
  const emphasis = resolveActionEmphasis(action);
  const emphasisClass = tailwindTokens.components.action.emphasis[emphasis];
  return (
    <button
      key={action.id}
      type={action.intent === "submit" ? "submit" : "button"}
      className={`${tailwindTokens.components.action.base} ${emphasisClass}`}
    >
      {action.label}
    </button>
  );
};

const renderForm = (intent: FormCreateIntent): React.ReactElement => {
  const layoutClass = tailwindTokens.layouts[resolvePattern(intent)];
  return (
    <div className={tailwindTokens.components.container}>
      <div className={layoutClass}>
        {intent.content?.title ? <h2>{intent.content.title}</h2> : null}
        <form className={tailwindTokens.components.section}>
          {intent.components.fields.map(renderField)}
        </form>
        <div className={tailwindTokens.components.actionsRow}>
          {intent.components.actions.map(renderAction)}
        </div>
      </div>
    </div>
  );
};

const renderTable = (intent: TableCreateIntent): React.ReactElement => {
  const layoutClass = tailwindTokens.layouts[resolvePattern(intent)];
  return (
    <div className={tailwindTokens.components.container}>
      <div className={layoutClass}>
        {intent.content?.title ? <h2>{intent.content.title}</h2> : null}
        <div className={tailwindTokens.components.table.wrapper}>
          <table className={tailwindTokens.components.table.base}>
            <thead>
              <tr>
                {intent.components.columns.map((column) => (
                  <th key={column.id} className={tailwindTokens.components.table.headerCell}>
                    {column.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                {intent.components.columns.map((column) => (
                  <td key={column.id} className={tailwindTokens.components.table.bodyCell}>
                    —
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
        {intent.components.actions.length > 0 ? (
          <div className={tailwindTokens.components.actionsRow}>
            {intent.components.actions.map(renderAction)}
          </div>
        ) : null}
      </div>
    </div>
  );
};

const renderModal = (intent: ModalOpenIntent): React.ReactElement => (
  <div className={tailwindTokens.components.modal.container}>
    <div className={tailwindTokens.components.modal.content}>
      {intent.content?.title ? <h2>{intent.content.title}</h2> : null}
      {intent.content?.body ? <p>{intent.content.body}</p> : null}
      <div className={tailwindTokens.components.modal.actions}>
        {intent.components.actions.map(renderAction)}
      </div>
    </div>
  </div>
);

const renderAlert = (intent: AlertShowIntent): React.ReactElement => (
  <div className={tailwindTokens.components.alert.base}>
    {intent.content?.body ?? ""}
  </div>
);

const renderCta = (intent: CtaRequestIntent): React.ReactElement => (
  <div className={tailwindTokens.components.cta.base}>
    {intent.content?.body ? <p>{intent.content.body}</p> : null}
    <div className={tailwindTokens.components.cta.actions}>
      {intent.components.actions.map(renderAction)}
    </div>
  </div>
);

const renderWithPatterns = (intent: UiIntent): React.ReactElement | null => {
  const pattern = selectPattern(intent, tailwindPatterns);
  if (!pattern) {
    return null;
  }
  return pattern.render(intent, { tokens: tailwindTokens });
};

const renderPage = (intent: PageCreateIntent): React.ReactElement => {
  const layoutClass = tailwindTokens.layouts[resolvePattern(intent)];
  return (
    <div className={tailwindTokens.components.container}>
      <div className={layoutClass}>
        {intent.sections.map((section) => (
          <section key={section.id} className={tailwindTokens.components.section}>
            {section.title ? <h3>{section.title}</h3> : null}
            {section.description ? <p>{section.description}</p> : null}
            {intent.components.actions
              .filter((action) => section.componentIds.includes(action.id))
              .map(renderAction)}
          </section>
        ))}
      </div>
    </div>
  );
};

export const tailwindAdapter: TailwindAdapter<React.ReactElement> = {
  id: "tailwind.react.adapter",
  version: "0.1.0",
  tokens: tailwindTokens,
  patterns: layoutPatterns,
  resolvePattern,
  componentMapping: {
    field: (field) => renderField(field),
    columnHeader: (column) => (
      <span className={tailwindTokens.components.table.headerCell}>{column.label}</span>
    ),
    action: (action) => renderAction(action),
  },
  render: (intent: ValidatedUiIntent) => {
    const patternOutput = renderWithPatterns(intent);
    if (patternOutput) {
      return patternOutput;
    }
    switch (intent.type) {
      case "page.create":
        return renderPage(intent);
      case "form.create":
        return renderForm(intent);
      case "table.create":
        return renderTable(intent);
      case "modal.open":
        return renderModal(intent);
      case "alert.show":
        return renderAlert(intent);
      case "cta.request":
        return renderCta(intent);
      default:
        return renderCta({
          ...intent,
          type: "cta.request",
        } as CtaRequestIntent);
    }
  },
};

export const resolveAdapterLayout = (intent: UiIntent): string => {
  const pattern = resolvePattern(intent);
  return tailwindTokens.layouts[pattern];
};
