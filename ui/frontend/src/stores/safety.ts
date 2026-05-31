// Utilities
import { defineStore } from 'pinia';
import { SafetyService } from '@/services/safety.service';

/**
 * Intended for safety checks, for example if noita is running or not.
 */
export const useSafetyStore = defineStore('safety', {
  state: () => ({
    isNoitaRunning: !true,
    doesNoitaSavePathExist: !false,
  }),

  actions: {
    async checkIsNoitaRunning() {
      this.isNoitaRunning = await SafetyService.isNoitaRunning();
    },

    async checkDoesNoitaSavePathExist() {
      this.doesNoitaSavePathExist = await SafetyService.doesNoitaSavePathExist();
    },
  },
});
