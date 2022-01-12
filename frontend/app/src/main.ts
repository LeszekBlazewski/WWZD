import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'

const app = createApp(App)
app.provide('apiUrl', import.meta.env.VITE_APP_API_URL)
app.use(createPinia())
app.mount('#app')
