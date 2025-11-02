import type { ApiResponse } from "@/interfaces/api-response";

/**
 * Validates the API response and throws an error if the response indicates failure.
 * @param response - The response from the backend
 * @param operationName - Name of the operation for error context
 * @throws Error if response.success is false
 */
export const validateResponse = <T>(
  response: ApiResponse<T>,
  operationName: string
): T => {
  if (!response.success && response.error) {
    const errorMessage = `${operationName} failed: [${response.error.type}] ${response.error.message}`;
    throw new Error(errorMessage);
  }

  if (!response.success) {
    throw new Error(`${operationName} failed with an unknown error`);
  }

  return response.data as T;
};
