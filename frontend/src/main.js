import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import 'bulma/css/bulma.css'
import './index.css'
import { fetchCurrentUser } from '@/composables/useAuth.js'

async function bootstrap() {
  await fetchCurrentUser()

  const app = createApp(App)
  app.use(router)
  app.use(Toast)
  app.mount('#app')
}

bootstrap()