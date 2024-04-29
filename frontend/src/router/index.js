import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import HomeView from '~/views/HomeView.vue'
import LoginView from '~/views/LoginView.vue'
import ProfileView from '~/views/ProfileView.vue'
import BookView from '~/views/BookView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/me',
      name: 'profile',
      component: ProfileView,
      meta: {
        authRequired: true,
      }
    },
    {
      path: '/book/:bookId',
      name: 'book',
      component: BookView,
    },
  ]
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.authRequired && !authStore.authorized)
    return {
      name: 'login',
      replace: true,
      query: { redirect: to.fullPath },
    }
})

export default router
