import type { DialogApi } from './DialogApi';
import { inject } from 'vue';
import { dialogApiKey } from './dialogApiKey';

export function useDialog(): DialogApi['showDialog'] {
  const dialogApi = inject(dialogApiKey, null);

  if (dialogApi === null) {
    throw new Error('DialogProvider is missing in the component tree.');
  }

  return dialogApi.showDialog;
}
