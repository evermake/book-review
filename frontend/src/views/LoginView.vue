<script setup>
import { storeToRefs } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import XButton from '~/components/XButton.vue';
import { useAuthStore } from '~/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { loading, authorized } = storeToRefs(authStore)
const username = ref('')
const password = ref('')
const disabled = computed(() => authorized.value || loading.value)
const error = ref('')

watch(authorized, (newAuthorized) => {
  if (newAuthorized)
    if (route.query.redirect)
      router.replace(route.query.redirect)
    else
      router.replace({ name: 'home' })
}, { immediate: true })

function handleBlur() {
  error.value = ''
}

function handleSubmit() {
  authStore
    .login(username.value, password.value)
    .catch((e) => {
      if (e instanceof Error)
        error.value = e.message
      else
        error.value = `${e}`
    })
}
</script>

<template>
  <form
    @submit.prevent="handleSubmit"
    class="mx-auto f-full max-w-300px flex flex-col gap-2"
  >
    <h1 class="text-center text-lg font-medium">Login</h1>
    <input
      v-model="username"
      :disabled="disabled"
      @blur="handleBlur"
      class="py-2 px-4 outline-none border focus-within:border-green"
      placeholder="Username"
      type="text"
      name="username"
    >
    <input
      v-model="password"
      :disabled="disabled"
      @blur="handleBlur"
      class="py-2 px-4 outline-none border focus-within:border-green"
      placeholder="Password"
      id="password"
      type="password"
      name="password"
    >
    <XButton type="submit">Login</XButton>
    <p v-if="error" class="text-sm text-red">{{ error }}</p>
  </form>
</template>
