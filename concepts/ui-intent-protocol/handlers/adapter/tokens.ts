import { TailwindAdapterTokens } from "./adapter-contract";

export const tailwindTokens: TailwindAdapterTokens = {
  spacing: {
    xs: "gap-2",
    sm: "gap-3",
    md: "gap-4",
    lg: "gap-6",
  },
  emphasis: {
    primary: "bg-slate-900 text-white",
    secondary: "border border-slate-300 text-slate-700",
    danger: "bg-red-600 text-white",
  },
  density: {
    compact: "text-sm",
    comfortable: "text-base",
  },
  layouts: {
    "single-column": "flex flex-col gap-6",
    "two-column": "grid grid-cols-1 gap-6 lg:grid-cols-2",
    "table-with-toolbar": "flex flex-col gap-4",
    "modal-centered": "flex flex-col gap-4",
    "alert-inline": "flex flex-col gap-2",
    "cta-inline": "flex flex-col gap-3",
  },
  components: {
    container: "w-full max-w-5xl mx-auto",
    section: "flex flex-col gap-4",
    actionsRow: "flex flex-wrap gap-2",
    field: {
      wrapper: "flex flex-col gap-1",
      label: "text-sm font-medium text-slate-700",
      control: "w-full rounded-md border border-slate-300 px-3 py-2",
      helper: "text-xs text-slate-500",
    },
    table: {
      wrapper: "w-full overflow-hidden rounded-md border border-slate-200",
      base: "w-full border-collapse",
      headerCell: "bg-slate-50 px-3 py-2 text-left text-xs uppercase tracking-wide text-slate-500",
      bodyCell: "border-t border-slate-200 px-3 py-2 text-sm text-slate-700",
    },
    action: {
      base: "inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium",
      emphasis: {
        primary: "bg-slate-900 text-white",
        secondary: "border border-slate-300 text-slate-700",
        danger: "bg-red-600 text-white",
      },
    },
    alert: {
      base: "rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700",
    },
    cta: {
      base: "rounded-md border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900",
      actions: "mt-3 flex flex-wrap gap-2",
    },
    modal: {
      container: "fixed inset-0 flex items-center justify-center bg-black/40",
      content: "w-full max-w-lg rounded-lg bg-white p-6",
      actions: "mt-4 flex justify-end gap-2",
    },
  },
};
