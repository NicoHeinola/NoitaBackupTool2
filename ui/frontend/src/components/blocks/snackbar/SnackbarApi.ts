import type { SnackbarDismissReason } from './SnackbarDismissReason';
import type { SnackbarOptions } from './SnackbarOptions';

export interface SnackbarApi {
  openSnackbar: (options: SnackbarOptions) => Promise<SnackbarDismissReason>;
}
