<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div v-if="!loadFailed && pageContent" class="text-center" background>
        <h1 class="text-h3 font-weight-bold">{{ pageTitle }}</h1>
        <div v-html="pageContent"  class="text-body-2 font-weight-light mb-n1"></div>
      </div>

      <v-alert v-else type="error" v-if="loadFailed">Página não encontrada.</v-alert>
      <div class="text-center" background v-else>
        <v-progress-circular  indeterminate />
      </div>
      
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const pageTitle = ref('')
const pageContent = ref('')
const loadFailed = ref(false)

const api = axios.create({
  baseURL:
    window.location.hostname === 'localhost'
      ? 'http://localhost:5000'
      : 'https://rua11storecatalogapi-production.up.railway.app',
  headers: { 'Content-Type': 'application/json' },
})

async function loadComponentFromAPI() {
  try {
    const pageName = 'Home Page' // nome da página com espaço
    const encodedPageName = encodeURIComponent(pageName) // transforma em "Home%20Page"
    const response = await api.get(`/pages/pages/${encodedPageName}`)

    pageTitle.value = response.data.title
    pageContent.value = response.data.content
    loadFailed.value = false
  } catch (error) {
    console.error('Erro ao buscar componente:', error)
    loadFailed.value = true
  }
}

onMounted(loadComponentFromAPI)
</script>
