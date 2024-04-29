import 'virtual:uno.css'
import '@unocss/reset/tailwind-compat.css'
import './assets/main.css'

import axios from 'axios'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'

import { ACCESS_TOKEN_STORAGE_KEY } from "./constants"
import App from './App.vue'
import router from './router'

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)

  if (token)
    config.headers.Authorization = `Bearer ${token}`

  return config
})

const app = createApp(App)
app.use(VueQueryPlugin)
app.use(createPinia())
app.use(router)
app.mount('#app')
