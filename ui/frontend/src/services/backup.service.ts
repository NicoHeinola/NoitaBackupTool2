import type Backup from "@/models/backup.model";

export const BackupService = {
  getBackups: async (): Promise<Backup[]> => {
    return (window as any).eel.get_backups()?.();
  },
};
