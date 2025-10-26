export const errorSnackbar = (
  openSnackbar: (opts: any) => void,
  error: any,
  isCustomError: boolean = false
) => {
  if (isCustomError) {
    openSnackbar({
      props: {
        text: error,
        color: "error",
      },
    });
    return;
  }

  const status = error?.response?.status;

  const details = error?.response?.data?.detail;

  if (status === 401) {
    openSnackbar({
      props: {
        text: "Unauthorized access.",
        color: "error",
      },
    });
  } else if (status === 403) {
    openSnackbar({
      props: {
        text: "Forbidden access.",
        color: "error",
      },
    });
  } else if (status === 404) {
    openSnackbar({
      props: {
        text: "Resource not found.",
        color: "error",
      },
    });
  } else if (status === 500) {
    openSnackbar({
      props: {
        text:
          "Internal server error. Details: " +
          (details
            ? JSON.stringify(details)
            : "No additional details provided."),
        color: "error",
      },
    });
  } else if (status === 422) {
    openSnackbar({
      props: {
        text: "Unprocessable entity.",
        color: "error",
      },
    });
  } else {
    openSnackbar({
      props: {
        text: "An unexpected error occurred.",
        color: "error",
      },
    });
  }

  console.error(error);
};
