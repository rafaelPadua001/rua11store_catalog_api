export default defineNuxtConfig({
  css: ['vuetify/styles/main.sass', '@mdi/font/css/materialdesignicons.min.css'],
  build: {
    transpile: ['vuetify'],
  },
})