import type { SnackbarDismissReason } from '@/components/blocks/snackbar/SnackbarDismissReason';
import type { SnackbarOptions } from '@/components/blocks/snackbar/SnackbarOptions';

export function errorSnackbar(
  openSnackbar: (opts: SnackbarOptions) => Promise<SnackbarDismissReason>,
  error: any,
  isCustomError = false,
) {
  if (isCustomError) {
    openSnackbar({
      message: error,
      color: 'error',
    });
    return;
  }

  // Parse error if it might be a stringified JSON
  try {
    const parsedError = JSON.parse(error.message);
    error = parsedError;
  } catch (parseError) {
    console.warn('Could not parse error message:', parseError);
  }

  const status = error?.response?.status;
  const details = error?.message;

  const fallbackMessage =
    'An unexpected error occurred. Details: ' +
    (details ? JSON.stringify(details) : 'No additional details provided.');

  switch (status) {
    case 401: {
      openSnackbar({ message: 'Unauthorized access.', color: 'error' });
      break;
    }
    case 403: {
      openSnackbar({ message: 'Forbidden access.', color: 'error' });
      break;
    }
    case 404: {
      openSnackbar({ message: 'Resource not found.', color: 'error' });
      break;
    }
    case 500: {
      openSnackbar({
        message:
          'Internal server error. Details: ' +
          (details
            ? JSON.stringify(details)
            : 'No additional details provided.'),
        color: 'error',
      });
      break;
    }
    case 422: {
      openSnackbar({ message: 'Unprocessable entity.', color: 'error' });
      break;
    }
    default: {
      openSnackbar({ message: fallbackMessage, color: 'error' });
    }
  }

  console.error(error);
}
