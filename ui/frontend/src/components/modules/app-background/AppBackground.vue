<script lang="ts" setup>
const images = ref(["/images/bg-1.png", "/images/bg-2.jpg"]);

const imageIndex = ref(Math.floor(Math.random() * images.value.length));

onMounted(() => {
  setInterval(() => {
    imageIndex.value = (imageIndex.value + 1) % images.value.length;
  }, 5000);
});
</script>

<template>
  <div class="position-absolute w-100 h-100">
    <div class="app-background-image">
      <v-fade-transition>
        <template v-for="(image, index) in images" :key="image">
          <v-img
            :src="image"
            class="fill-height position-absolute w-100 h-100"
            cover
            v-if="imageIndex === index"
          ></v-img>
        </template>
      </v-fade-transition>
      <div class="app-background-gradient"></div>
    </div>
  </div>
</template>

<style scoped>
.app-background-image {
  position: absolute;
  width: 100%;
  height: 242px;
}

.app-background-gradient {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: linear-gradient(
    to bottom,
    rgb(18, 18, 18, 60%),
    rgb(18, 18, 18, 1)
  );
}
</style>
