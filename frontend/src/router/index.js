import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import EventPage from '@/views/EventPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/event/:link',
    name: 'Event',
    component: EventPage,
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})