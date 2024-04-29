import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { isAxiosError } from 'axios'
import { useStorage } from '@vueuse/core'
import { useGetCurrentUserUsersMeGet, useTokenTokenPost } from '~/api'
import { ACCESS_TOKEN_STORAGE_KEY } from '~/constants'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = useStorage(ACCESS_TOKEN_STORAGE_KEY, null)
  const forcedLogout = ref(false)

  const getToken = useTokenTokenPost({
    mutation: {
      retry: (retryCount, error) => {
        if (isAuthError(error)) return false
        return retryCount < 3
      }
    }
  })

  const {
    data: meData,
    isLoading: meLoading,
    refetch: refetchMe,
  } = useGetCurrentUserUsersMeGet({
    query: {
      retry: (retryCount, error) => {
        if (isAuthError(error)) return false
        return retryCount < 3
      },
      enabled: !(forcedLogout.value) && Boolean(accessToken.value)
    },
  })

  const me = computed(() => (
    (!forcedLogout.value && meData.value)
      ? meData.value.data
      : null
  ))
  const loading = computed(() => Boolean(meLoading.value || getToken.isPending.value))
  const authorized = computed(() => Boolean(me.value))

  /**
   * @param {string} username 
   * @param {string} password 
   */
  async function login(username, password) {
    forcedLogout.value = false
    try {
      const result = await getToken.mutateAsync({
        data: { username, password }
      })
      accessToken.value = result.data.access_token
      refetchMe()
    } catch (err) {
      if (isAuthError(err))
        throw new Error('Invalid username or password.')
      throw err
    }
  }

  function logout() {
    forcedLogout.value = true
    accessToken.value = null
  }

  return {
    accessToken,
    forcedLogout,

    authorized,
    me,
    loading,
    login,
    logout
  }
})

/**
 * Returns boolean indicating whether the error is an error related to
 * authorization (401 or 403 status code).
 *
 * @param {AxiosError<any>} error 
 */
function isAuthError(error) {
  return (
    isAxiosError(error) && error.response && (
      error.response.status === 401 ||
      error.response.status === 403
    )
  )
}
