import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import App from './App.vue'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [] // Add your routes here
})

// Create Vuetify
const vuetify = createVuetify()

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')