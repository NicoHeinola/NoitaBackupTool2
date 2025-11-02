<script lang="ts" setup>
import type Backup from "@/models/backup.model";

const backup = defineModel<Backup>({
  default: {},
});
</script>

<template>
  <v-form>
    {{ backup.date }}
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="backup.name"
          label="Name"
          placeholder="Enter backup name"
          required
        />
      </v-col>
      <v-col cols="12">
        <v-textarea
          v-model="backup.description"
          label="Description"
          placeholder="Enter backup description"
          rows="3"
        />
      </v-col>
      <v-col cols="12">
        <v-text-field v-model="backup.date" label="Date" type="date" />
      </v-col>
    </v-row>
  </v-form>
</template>
