import { inject } from "vue";

type DialogOptions = {
  component: any; // The component to be rendered in the dialog
  props?: Record<string, any>;
};

type OpenDialogFn = (options: DialogOptions) => Promise<any>;

export function useDialog(): OpenDialogFn {
  const openDialog = inject<OpenDialogFn>("openDialog");
  if (!openDialog) {
    throw new Error("DialogProvider is missing in the component tree.");
  }
  return openDialog;
}
