// Utilities
import { defineStore } from "pinia";

export const useBackupStore = defineStore("backup", {
  state: () => ({
    lastSelectedBackupId: null as string | null,
  }),

  actions: {
    setLastSelectedBackupId(id: string | null) {
      this.lastSelectedBackupId = id;
    },
  },

  persist: true,
});
