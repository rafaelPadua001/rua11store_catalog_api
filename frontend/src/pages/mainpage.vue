<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div v-if="!loadFailed && pageContent" class="text-center" background>
        <h1 class="text-h3 font-weight-bold">{{ pageTitle }}</h1>
        <div v-html="pageContent" class="text-body-2 font-weight-light mb-n1"></div>

        <div class="mt-2 mb-4 d-flex justify-center">
          <v-item-group divided>
            <v-btn color="black" class="outline" size="small" href="https://example.com/download-ios-app.apk"
              target="_blank" variant="text" disabled>
              <v-icon class="mr-2" size="large">mdi-apple</v-icon>
              App iOS
            </v-btn>

            <v-btn color="black" class="outline" size="small" href="https://example.com/download-android-app.apk"
              target="_blank" variant="text">
              <v-icon class="mr-2" size="large">mdi-android</v-icon>
              App Android
            </v-btn>

            <v-btn color="primary" size="small" href="https://rua11store-web.vercel.app/" target="_blank"
              variant="text">
              <v-icon class="mr-2" size="large">mdi-store</v-icon>
              Loja Online
            </v-btn>
          </v-item-group>
        </div>

      </div>

      <v-alert v-else type="error" v-if="loadFailed">Página não encontrada.</v-alert>
      <div class="text-center" background v-else>
        <v-progress-circular indeterminate />
      </div>
    </v-responsive>
    <v-btn
  color="deep-purple"
  dark
  class="whatsapp-btn"
  href="https://wa.me/556191865680"
  target="_blank"
  elevation="10"
  icon
>
  <v-icon size="28">mdi-whatsapp</v-icon>
</v-btn>

  </v-container>

</template>


<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useHead } from '@vueuse/head'
import axios from 'axios'
import { useSeo } from '../useSeo'

const pageTitle = ref('')
const pageContent = ref('')
const loadFailed = ref(false)



const api = axios.create({
  baseURL:
    window.location.hostname === 'localhost'
      ? 'http://localhost:5000'
      : 'https://rua11store-catalog-api-lbp7.onrender.com/',
  headers: { 'Content-Type': 'application/json' },
})

const { setSeo } = useSeo()



async function loadComponentFromAPI() {
  try {
    const pageName = 'Home Page'
    const encodedPageName = encodeURIComponent(pageName)
    const response = await api.get(`/pages/pages/${encodedPageName}`)

    pageTitle.value = response.data.title
    pageContent.value = response.data.content
    loadFailed.value = false

    await loadSeoFromAPI(response.data.id)
  } catch (error) {
    console.error('Erro ao buscar componente:', error)
    loadFailed.value = true
  }
}

async function loadSeoFromAPI(pageId: number) {
  try {
    const response = await api.get(`/seo/seo/${pageId}`)
    const seoData = response.data.seo

    setSeo(seoData)  // atualiza SEO via composable
  } catch (error) {
    console.error('Erro ao buscar SEO:', error)
  }
}

onMounted(() => {
  loadComponentFromAPI()
})
</script>

<style scoped>
.whatsapp-btn {
  position: fixed;
  bottom: 50px;
  right: 20px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  min-width: 56px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
</style>

