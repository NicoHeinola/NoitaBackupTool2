import type { SnackbarColor } from './SnackbarColor';
import type { SnackbarLocation } from './SnackbarLocation';

export interface SnackbarOptions {
  message: string;
  color?: SnackbarColor;
  timeout?: number;
  location?: SnackbarLocation;
  closable?: boolean;
}
