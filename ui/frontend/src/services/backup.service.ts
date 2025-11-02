import type Backup from "@/models/backup.model";

export const BackupService = {
  getBackups: async (): Promise<Backup[]> => {
    return (window as any).eel.get_backups()?.();
  },

  saveBackup: async (backup: Backup): Promise<Backup> => {
    return (window as any).eel.save_backup?.(backup)?.();
  },

  deleteBackup: async (backupId: string): Promise<void> => {
    return (window as any).eel.delete_backup?.(backupId)?.();
  },

  loadBackup: async (backupId: string): Promise<void> => {
    return (window as any).eel.load_backup?.(backupId)?.();
  },

  duplicateBackup: async (backupId: string): Promise<Backup> => {
    return (window as any).eel.duplicate_backup?.(backupId)?.();
  },

  reloadBackup: async (backupId: string): Promise<void> => {
    return (window as any).eel.reload_backup?.(backupId)?.();
  },
};
