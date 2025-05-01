import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"
import { fetchCurrentUser } from '@/composables/useAuth.js'
import 'bulma/css/bulma.css'
import './index.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
app.use(Toast)

fetchCurrentUser()