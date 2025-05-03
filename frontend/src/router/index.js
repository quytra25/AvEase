import { createRouter, createWebHistory } from 'vue-router'
import CreateEvent from '@/views/CreateEvent.vue'
import EventList from '@/views/EventList.vue'
import EventDetail from '@/views/EventDetail.vue'
import Login from '@/views/Login.vue'
import { fetchCurrentUser, useAuth } from '@/composables/useAuth'

const routes = [
  { path: '/', name: 'Home', component: CreateEvent },
  { path: '/events', name: 'EventList', component: EventList },
  { path: '/events/:link', name: 'EventDetail', component: EventDetail, props: true },
  { path: '/login', name: 'Login', component: Login },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach(async (to, from, next) => {
  await fetchCurrentUser()
  const { isAuthenticated } = useAuth()
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return next({ path: '/login' })
  }
  next()
})

export default router