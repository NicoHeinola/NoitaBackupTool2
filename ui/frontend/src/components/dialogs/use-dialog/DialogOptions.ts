export interface DialogOptions<
  Props extends Record<string, unknown> = Record<string, never>,
> {
  component: any;
  props?: Props;
  closeDelay?: number;
}
