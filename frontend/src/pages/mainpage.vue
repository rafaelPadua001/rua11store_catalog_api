<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div v-if="!loadFailed && pageContent" class="text-center">
        <v-img v-if="logoImage" :src="logoImage" :alt="pageTitle" width="175" height="175" contain
          class="mb-n4 mx-auto d-block" />

        <div class="mt-0 mb-16 d-flex justify-center flex-wrap">
          <v-row justify="center">
            <v-col cols="12" md="12" sm="6" class="d-flex justify-center">
              <!-- seus botões aqui -->
              <v-btn class="mx-0" color="black" size="small" href="https://example.com/download-ios-app.apk"
                target="_blank" disabled>
                <v-icon class="mr-0" size="large">mdi-apple</v-icon>
                App iOS
              </v-btn>
              <v-btn class="mx-1" color="black" size="small" href="https://example.com/download-android-app.apk"
                target="_blank">
                <v-icon class="mr-0" size="large" color="success">mdi-android</v-icon>
                App Android
              </v-btn>
              <v-btn class="mx-0" color="primary" size="small" href="https://rua11store-web.vercel.app/"
                target="_blank">
                <v-icon class="mr-0" size="large">mdi-store</v-icon>
                Acessar Loja
              </v-btn>
            </v-col>
          </v-row>
        </div>

        <v-row justify="center" class="my-2">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-carousel :show-arrows="false" cycle hide-delimiters height="250" interval="500000" v-model="activeIndex">
              <v-carousel-item v-for="(chunk, index) in chunkedProducts" :key="index">
                <div class="d-flex justify-center" style="gap: 8px;">
                  <v-img v-for="product in chunk" :key="product.name" :src="product.image_path"
                    :alt="product.seo?.slug || product.name" max-width="200" max-height="200" contain />
                </div>
              </v-carousel-item>
            </v-carousel>
          </v-col>
        </v-row>
      </div>

      <v-alert v-else-if="loadFailed" type="error">Página não encontrada.</v-alert>
      <div v-else class="text-center" background>
        <v-progress-circular indeterminate />
      </div>
    </v-responsive>

    <v-btn color="deep-purple" dark class="whatsapp-btn" href="https://wa.me/556191865680" target="_blank"
      elevation="10" icon>
      <v-icon size="28">mdi-whatsapp</v-icon>
    </v-btn>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useSeo } from '../useSeo'
import logoImage from '../assets/rua11store_logo.png'

const loadFailed = ref(false)
const pageTitle = ref('')
const pageContent = ref('')

interface Product {
  name: string
  image_path: string
  seo?: {
    slug: string
    meta_title?: string
    meta_description?: string
    keywords?: string
  }
}

const productsData = ref<Product[]>([])
const activeIndex = ref(0)

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

    setSeo(seoData)
  } catch (error) {
    console.error('Erro ao buscar SEO:', error)
  }
}

async function loadProductsToCarousel() {
  try {
    const response = await api.get(`/products`)
    productsData.value = response.data
  } catch (error) {
    console.error('Erro ao buscar produtos:', error)
  }
}

// Computed que divide o array em pedaços (chunks) de 3 produtos
const chunkSize = 3
const chunkedProducts = computed(() => {
  const chunks = []
  for (let i = 0; i < productsData.value.length; i += chunkSize) {
    chunks.push(productsData.value.slice(i, i + chunkSize))
  }
  return chunks
})

onMounted(() => {
  loadComponentFromAPI()
  loadProductsToCarousel()

  // Atualiza o slide ativo automaticamente a cada 3s
  setInterval(() => {
    const maxIndex = chunkedProducts.value.length - 1
    activeIndex.value = activeIndex.value >= maxIndex ? 0 : activeIndex.value + 1
  }, 5000)
})
</script>

<style scoped>
.v-btn {
  margin-left: 1px !important;
  margin-right: 1px !important;
}

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

.mx-auto.text-center {
  max-width: 100%;
  padding-left: 10px;
  padding-right: 10px;
}
</style>
