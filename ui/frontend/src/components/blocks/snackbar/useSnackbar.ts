import type { SnackbarApi } from './SnackbarApi';
import { inject } from 'vue';
import { snackbarApiKey } from './snackbarApiKey';

export function useSnackbar(): SnackbarApi['openSnackbar'] {
  const snackbar = inject(snackbarApiKey, null);

  if (snackbar === null) {
    throw new Error('SnackbarProvider is missing in the component tree.');
  }

  return snackbar.openSnackbar;
}
