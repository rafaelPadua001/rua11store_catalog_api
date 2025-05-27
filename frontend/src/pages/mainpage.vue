<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div v-if="!loadFailed && pageContent" class="text-center" background>
        <h1 class="text-h3 font-weight-bold">{{ pageTitle }}</h1>
        <div v-html="pageContent" class="text-body-2 font-weight-light mb-n1"></div>
      </div>

      <v-alert v-else type="error" v-if="loadFailed">Página não encontrada.</v-alert>
      <div class="text-center" background v-else>
        <v-progress-circular indeterminate />
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useHead } from '@vueuse/head'
import axios from 'axios'

const pageTitle = ref('')
const pageContent = ref('')
const loadFailed = ref(false)

const metaTitle = ref('')
const metaDescription = ref('')
const metaKeywords = ref('')
const ogTitle = ref('')
const ogDescription = ref('')
const ogImage = ref('')

const api = axios.create({
  baseURL:
    window.location.hostname === 'localhost'
      ? 'http://localhost:5000'
      : 'https://rua11storecatalogapi-production.up.railway.app',
  headers: { 'Content-Type': 'application/json' },
})

// 🧠 Bind reativo com useHead
useHead({
  title: metaTitle,
  meta: [
    { name: 'description', content: metaDescription },
    { name: 'keywords', content: metaKeywords },
    { property: 'og:title', content: ogTitle },
    { property: 'og:description', content: ogDescription },
    { property: 'og:image', content: ogImage },
  ],

})

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
    

    metaTitle.value = seoData.metaTitle || ''
    metaDescription.value = seoData.metaDescription || ''
    metaKeywords.value = seoData.metaKeywords || ''
    ogTitle.value = seoData.ogTitle || ''
    ogDescription.value = seoData.ogDescription || ''
    ogImage.value = seoData.ogImage || ''
  } catch (error) {
    console.error('Erro ao buscar SEO:', error)
  }
}

onMounted(() => {
  loadComponentFromAPI()
})
</script>
