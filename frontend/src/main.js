import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import 'bulma/css/bulma.css'
import './index.css'
import { useAuth } from '@/composables/useAuth.js'
import api from '@/services/api'
import '@fortawesome/fontawesome-free/css/all.css'

async function bootstrap() {
    try {
        await api.getCsrfToken();
    } catch (err) {
        console.warn('CSRF cookie fetch failed', err);
    }

    const { fetchCurrentUser } = useAuth()
    await fetchCurrentUser()
    
    const app = createApp(App)
    app.use(router)
    app.use(Toast)
    app.mount('#app')
}

bootstrap()