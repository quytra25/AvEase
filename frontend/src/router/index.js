import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import EventDetail from '@/components/EventDetail.vue'
import Login from '@/components/Login.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/events/:id', name: 'Detail', component: EventDetail, props: true },
  { path: '/login', name: 'Login', component: Login },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})