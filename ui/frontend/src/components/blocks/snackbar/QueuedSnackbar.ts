import type { SnackbarColor } from './SnackbarColor';
import type { SnackbarDismissReason } from './SnackbarDismissReason';
import type { SnackbarLocation } from './SnackbarLocation';

export interface QueuedSnackbar {
  text: string;
  color: SnackbarColor;
  timeout: number;
  location: SnackbarLocation;
  closable: boolean;
  variant: 'tonal';
  onDismiss?: (reason: SnackbarDismissReason) => void;
}
