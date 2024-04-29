import { storeToRefs } from 'pinia'
import { watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

export default function useProtection() {
  const authStore = useAuthStore()
  const router = useRouter()
  const route = useRoute()
  const { authorized, loading } = storeToRefs(authStore)

  watch([authorized, loading], ([newAuthorized, newLoading]) => {
    if (!newLoading && !newAuthorized) {
      router.replace({
        name: 'login',
        replace: true,
        query: { redirect: route.fullPath },
      })
    }
  }, { immediate: true })
}
