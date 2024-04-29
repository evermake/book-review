<script setup>
import XButton from '~/components/XButton.vue'
import useProtection from '~/composables/useProtection'
import { useAuthStore } from '~/stores/auth'

const { logout, me } = useAuthStore()
useProtection()
</script>

<template>
  <main>
    <h1 class="font-medium text-xl text-center">Welcome, {{ me.login }}!</h1>
    <XButton color="red" @click="logout">Logout</XButton>
  </main>
</template>
