import type Backup from "@/models/backup.model";
import { validateResponse } from "@/utils/response";

export const BackupService = {
  getBackups: async (): Promise<Backup[]> => {
    const response = await (window as any).eel.get_backups()?.();
    return validateResponse<Backup[]>(response, "Get backups");
  },

  saveBackup: async (backup: Backup): Promise<Backup> => {
    const response = await (window as any).eel.save_backup?.(backup)?.();
    return validateResponse<Backup>(response, "Save backup");
  },

  deleteBackup: async (backupId: string): Promise<void> => {
    const response = await (window as any).eel.delete_backup?.(backupId)?.();
    validateResponse<void>(response, "Delete backup");
  },

  loadBackup: async (backupId: string): Promise<void> => {
    const response = await (window as any).eel.load_backup?.(backupId)?.();
    validateResponse<void>(response, "Load backup");
  },

  duplicateBackup: async (backupId: string): Promise<Backup> => {
    const response = await (window as any).eel.duplicate_backup?.(backupId)?.();
    return validateResponse<Backup>(response, "Duplicate backup");
  },

  replaceBackup: async (backupId: string): Promise<void> => {
    const response = await (window as any).eel.replace_backup?.(backupId)?.();
    validateResponse<void>(response, "Replace backup");
  },
};
