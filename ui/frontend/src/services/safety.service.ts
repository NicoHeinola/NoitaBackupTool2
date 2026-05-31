import { validateResponse } from '@/utils/response';

export const SafetyService = {
  isNoitaRunning: async (): Promise<boolean> => {
    const response = await (window as any).eel.is_noita_running()?.();
    return validateResponse<boolean>(response, 'Is Noita running?');
  },

  doesNoitaSavePathExist: async (): Promise<boolean> => {
    const response = await (window as any).eel.does_noita_save_path_exist()?.();
    return validateResponse<boolean>(response, 'Does Noita save path exist?');
  },
};
