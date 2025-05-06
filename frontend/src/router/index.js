import { createRouter, createWebHistory } from 'vue-router'
import CreateEvent from '@/views/CreateEvent.vue'
import EventList from '@/views/EventList.vue'
import EventDetail from '@/views/EventDetail.vue'
import Login from '@/views/Login.vue'
import { useAuth } from '@/composables/useAuth'
import EditEvent from '@/views/EditEvent.vue'

const routes = [
  { path: '/', name: 'Home', component: CreateEvent },
  { path: '/events', name: 'EventList', component: EventList },
  { path: '/events/:link', name: 'EventDetail', component: EventDetail, props: true },
  { path: '/login', name: 'Login', component: Login },
  { path: '/events/:link/edit', name: 'EditEvent', component: EditEvent}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach(async (to, from, next) => {
  const { fetchCurrentUser } = useAuth()
  await fetchCurrentUser()
  next()
})

export default router