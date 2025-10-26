<script lang="ts" setup>
import { useSnackbar } from "@/components/blocks/snackbar/useSnackbar";
import { BackupService } from "@/services/backup.service";
import { errorSnackbar } from "@/utils/errorSnackbar";
import type Backup from "@/models/backup.model";

const props = withDefaults(
  defineProps<{
    backup?: Backup;
  }>(),
  {
    backup: undefined,
  }
);

const openSnackbar = useSnackbar();

const backupData = ref<Backup>({
  id: props.backup?.id,
  name: props.backup?.name || "",
  description: props.backup?.description || "",
  date: props.backup?.date,
});

const emit = defineEmits<{
  (e: "resolve", payload: boolean): void;
  (e: "close"): void;
}>();

const loading = ref(false);

const isEditMode = computed(() => !!props.backup?.id);

const save = async () => {
  loading.value = true;
  try {
    await BackupService.saveBackup(backupData.value);
    openSnackbar({
      props: {
        text: isEditMode.value
          ? "Backup updated successfully."
          : "Backup created successfully.",
        color: "success",
      },
    });
    emit("resolve", true);
  } catch (error) {
    console.error("Error saving backup:", error);
    errorSnackbar(
      openSnackbar,
      isEditMode.value
        ? "Failed to update backup."
        : "Failed to create backup.",
      true
    );
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <v-card>
    <v-card-title>
      {{ isEditMode ? "Edit Backup" : "Add Backup" }}
    </v-card-title>
    <v-card-text>
      <edit-backups-form v-model="backupData" />
    </v-card-text>
    <v-card-actions class="d-flex justify-end">
      <v-btn
        variant="outlined"
        color="error"
        :disabled="loading"
        @click="emit('resolve', false)"
      >
        Cancel
      </v-btn>
      <v-btn
        variant="elevated"
        color="success"
        :loading="loading"
        @click="save()"
      >
        {{ isEditMode ? "Update" : "Create" }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
