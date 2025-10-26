import { inject } from "vue";

type SnackbarOptions = {
  props?: Record<string, any>;
};

type OpenSnackbarFn = (options: SnackbarOptions) => Promise<any>;

export function useSnackbar(): OpenSnackbarFn {
  const openSnackbar = inject<OpenSnackbarFn>("openSnackbar");
  if (!openSnackbar) {
    throw new Error("SnackbarProvider is missing in the component tree.");
  }
  return openSnackbar;
}
