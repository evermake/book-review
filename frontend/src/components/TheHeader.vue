<script setup>
import { storeToRefs } from 'pinia'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const { loading, me } = storeToRefs(authStore)
</script>

<template>
  <header class="py-2 flex justify-between items-center border-b">
    <div class="flex justify-between items-center gap-2">
      <RouterLink :to="{ name: 'home' }">📚 Book Review</RouterLink>
    </div>

    <div class="flex justify-between items-center gap-2">
      <span v-if="loading">...</span>
      <RouterLink v-else-if="me" :to="{ name: 'profile' }">Profile</RouterLink>
      <RouterLink v-else :to="{ name: 'login' }">Login</RouterLink>
    </div>
  </header>
</template>
