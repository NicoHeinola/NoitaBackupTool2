export const SettingService = {
  getAllSettings: async (): Promise<Record<string, any>> => {
    return (window as any).eel.get_all_settings()?.();
  },

  getSetting: async (key: string, defaultValue: any = "") => {
    return (window as any).eel.get_setting?.(key, defaultValue)?.();
  },

  saveSetting: async (key: string, value: any) => {
    return (window as any).eel.save_setting?.(key, value)?.();
  },

  saveSettings: async (settings: Record<string, any>) => {
    return (window as any).eel.save_settings?.(settings)?.();
  },
};
