// main.ts

import { createApp } from 'vue'
import App from './App.vue'
import 'vuetify/styles'

// Plugins
import { registerPlugins } from '@/plugins'

// Importando o head manager
import { createHead } from '@vueuse/head'

//Pixel facebook
import { initMetaPixel } from "@/plugins/meta-pixel";



const app = createApp(App)

initMetaPixel("801771992806957")

// Cria o gerenciador de head
const head = createHead()
app.use(head)

registerPlugins(app)

app.mount('#app')
