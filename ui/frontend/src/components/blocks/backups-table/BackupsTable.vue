<script lang="ts" setup>
import { BackupService } from "@/services/backup.service";
import { useSnackbar } from "../snackbar/useSnackbar";

const backups = ref([]);

const openSnackbar = useSnackbar();

const getBackups = async () => {
  try {
    backups.value = await BackupService.getBackups();
  } catch (error) {
    console.error("Error fetching backups:", error);
    openSnackbar({
      props: {
        text: "Failed to load backups.",
        color: "error",
      },
    });
  }
};

onMounted(getBackups);
</script>

<template>
  Backups: {{ backups }}
  <v-data-table></v-data-table>
</template>
