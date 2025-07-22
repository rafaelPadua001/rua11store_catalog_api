<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div v-if="!loadFailed && pageContent" class="text-center">
        <div>
          <v-img v-if="logoImage" :src="logoImage" :alt="logoImage" width="175" height="175" contain
            class="mb-n4 mx-auto d-block"></v-img>

        </div>
        <div class="mt-0 mb-16 d-flex justify-center flex-wrap">
          <v-row>
            <v-col>
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
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-slide-group show-arrows>
                <v-slide-group-item v-for="(product, index) in productsData" :key="index">
                  <v-img :src="product.image_path" :alt="product.seo?.slug" height="200" width="200" class="mx-2" cover />
                </v-slide-group-item>
              </v-slide-group>

            </v-col>
          </v-row>

        </div>



      </div>

      <v-alert v-else type="error" v-if="loadFailed">Página não encontrada.</v-alert>
      <div class="text-center" background v-else>
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
import { ref, onMounted, watch } from 'vue'
import { useHead } from '@vueuse/head'
import axios from 'axios'
import { useSeo } from '../useSeo'
import logoImage from '../assets/rua11store_logo.png'

const loadFailed = ref(false)
const pageTitle = ref('')
const pageContent = ref('')

interface Product {
  name: string
  image_path: string
  // adicione mais campos se necessário
}

const productsData = ref<Product[]>([])





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

async function loadProductsToCarrosel() {
  try {
    const response = await api.get(`/products`)
    productsData.value = response.data;
    return productsData;

  }
  catch {

  }
}



onMounted(() => {
  loadComponentFromAPI()
  loadProductsToCarrosel();
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
</style>
