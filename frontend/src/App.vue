<script setup>
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue';
</script>

<template>
  <div class="container mx-auto">
    <TheHeader />
    <main class="py-6">
      <RouterView />
    </main>
  </div>
</template>
