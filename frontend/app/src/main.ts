import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.provide('apiUrl', import.meta.env.VITE_APP_API_URL)
app.mount('#app')
