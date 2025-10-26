<script lang="ts" setup>
import type Backup from "@/models/backup.model";

const backup = defineModel<Backup>({
  default: {},
});
</script>

<template>
  <v-form>
    <v-row>
      <v-col cols="12">
        <v-text-field
          hide-details
          label="Name"
          v-model="backup.name"
          placeholder="Enter backup name"
          required
        />
      </v-col>
      <v-col cols="12">
        <v-textarea
          hide-details
          label="Description"
          v-model="backup.description"
          placeholder="Enter backup description"
          rows="3"
        />
      </v-col>
    </v-row>
  </v-form>
</template>
