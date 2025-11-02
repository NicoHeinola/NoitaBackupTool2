export interface ApiResponse<T = any> {
  success: boolean;
  data: T | null;
  error: {
    type: string;
    message: string;
  } | null;
}
