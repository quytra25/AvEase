import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import CreateEvent from '@/views/CreateEvent.vue'
import EventList   from '@/views/EventList.vue'
import EventDetail from '@/views/EventDetail.vue'
import Login from '@/views/Login.vue'
import { fetchCurrentUser, useAuth } from '@/composables/useAuth'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/CreateEvent.vue') },
  { path: '/events', name: 'EventList', component: EventList },
  { path: '/events/:id', name: 'Detail', component: EventDetail, props: true },
  { path: '/login', name: 'Login', component: Login },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard pages, for users who are logged in
router.beforeEach(async (to, from, next) => {
  await fetchCurrentUser()
  const { isAuthenticated } = useAuth()
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return next({ path: '/login' })
  }
  next()
})

export default router