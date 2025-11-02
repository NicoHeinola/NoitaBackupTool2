import { validateResponse } from "@/utils/response";

export const SettingService = {
  getAllSettings: async (): Promise<Record<string, any>> => {
    const response = await (window as any).eel.get_all_settings()?.();
    return validateResponse<Record<string, any>>(response, "Get all settings");
  },

  getSetting: async (key: string, defaultValue: any = "") => {
    const response = await (window as any).eel.get_setting?.(
      key,
      defaultValue
    )?.();
    return validateResponse<any>(response, "Get setting");
  },

  saveSetting: async (key: string, value: any) => {
    const response = await (window as any).eel.save_setting?.(key, value)?.();
    return validateResponse<void>(response, "Save setting");
  },

  saveSettings: async (settings: Record<string, any>) => {
    const response = await (window as any).eel.save_settings?.(settings)?.();
    return validateResponse<void>(response, "Save settings");
  },
};
