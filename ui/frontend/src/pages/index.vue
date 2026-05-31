<script lang="ts" setup>
import type BackupsTable from '@/components/blocks/backups-table/BackupsTable.vue';
import type Backup from '@/models/backup.model';
import TooltipIcon from '@/components/blocks/tooltip-icon/TooltipIcon.vue';
import EditBackupsDialog from '@/components/dialogs/edit-backups-dialog/EditBackupsDialog.vue';
import EditSettingsDialog from '@/components/dialogs/edit-settings-dialog/EditSettingsDialog.vue';
import { useDialog } from '@/components/dialogs/use-dialog/useDialog';

const openDialog = useDialog();
const backupsTableRef = ref<InstanceType<typeof BackupsTable> | null>(null);

const searchFilter = ref<string>('');

const openEditSettingsDialog = async () => {
  await openDialog({
    component: EditSettingsDialog,
  });
};

const handleAddBackup = async () => {
  const result = await openDialog({
    component: EditBackupsDialog,
  });

  if (result) {
    await backupsTableRef.value?.getBackups();
  }
};

const filterBackup = (backup: Backup): boolean => {
  const filter = searchFilter.value.toLowerCase();
  return (
    !!backup.name?.toLowerCase().includes(filter) ||
    !!backup.description?.toLowerCase().includes(filter) ||
    !!backup.date?.toLowerCase().includes(filter)
  );
};
</script>

<template>
  <v-container class="w-100 h-100 my-12">
    <v-row>
      <v-col class="d-flex align-center justify-space-between ga-2" cols="12">
        <h1 class="text-primary text-primary header-1">Noita Backups</h1>
        <div class="d-flex align-center ga-2">
          <v-btn prepend-icon="mdi-plus" @click="handleAddBackup">
            Backup current save
          </v-btn>
          <tooltip-icon text="This will copy and zip your current save file." />
        </div>
      </v-col>

      <v-col cols="12">
        <v-text-field v-model="searchFilter" label="Search for backups" />
      </v-col>
      <v-col cols="12">
        <backups-table ref="backupsTableRef" :filter-fn="filterBackup" />
      </v-col>
    </v-row>
  </v-container>
  <floating-button
    color="secondary"
    icon="mdi-cog"
    @click.stop="() => openEditSettingsDialog()"
  />
</template>

<style lang="scss" scoped>
.header-1 {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
</style>
