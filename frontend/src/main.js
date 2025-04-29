import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './index.css'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

app.use(Toast)

createApp(App).use(router).mount('#app')