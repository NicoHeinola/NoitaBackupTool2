export const BackupService = {
  getBackups: async () => {
    console.log("WINDOW", window);

    return (window as any).eel.get_backups()?.();
  },
};
