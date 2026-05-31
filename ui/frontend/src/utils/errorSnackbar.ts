export function errorSnackbar(openSnackbar: (opts: any) => void, error: any, isCustomError = false) {
  if (isCustomError) {
    openSnackbar({
      props: {
        text: error,
        color: 'error',
      },
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

  switch (status) {
    case 401: {
      openSnackbar({
        props: {
          text: 'Unauthorized access.',
          color: 'error',
        },
      });

      break;
    }
    case 403: {
      openSnackbar({
        props: {
          text: 'Forbidden access.',
          color: 'error',
        },
      });

      break;
    }
    case 404: {
      openSnackbar({
        props: {
          text: 'Resource not found.',
          color: 'error',
        },
      });

      break;
    }
    case 500: {
      openSnackbar({
        props: {
          text:
            'Internal server error. Details: ' +
            (details ? JSON.stringify(details) : 'No additional details provided.'),
          color: 'error',
        },
      });

      break;
    }
    case 422: {
      openSnackbar({
        props: {
          text: 'Unprocessable entity.',
          color: 'error',
        },
      });

      break;
    }
    default: {
      openSnackbar({
        props: {
          text:
            'An unexpected error occurred. Details: ' +
            (details ? JSON.stringify(details) : 'No additional details provided.'),
          color: 'error',
        },
      });
    }
  }

  console.error(error);
}
