import type { DialogOptions } from './DialogOptions';

export interface DialogApi {
  showDialog: <
    Result = unknown,
    Props extends Record<string, unknown> = Record<string, never>,
  >(
    options: DialogOptions<Props>,
  ) => Promise<Result | undefined>;
}
