<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div v-if="!loadFailed && pageContent" class="text-center">
        <v-img v-if="logoImage" :src="logoImage" :alt="pageTitle" width="175" height="175" contain
          class="mb-n4 mx-auto d-block" />

        <div class="mt-0 mb-2 d-flex justify-center flex-wrap">
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
        <div class="mt-0 mb-1 d-flex justify-center flex-wrap">
          <v-row justify="center" class="my-2">
            <v-col cols="12" sm="10" md="8" lg="6">
              <v-carousel :show-arrows="false" cycle hide-delimiters height="250" interval="500000"
                v-model="activeIndex">
                <v-carousel-item v-for="(chunk, index) in chunkedProducts" :key="index">
                  <div style="display: flex; justify-content: center; gap: 1px;">
                    <template v-for="product in chunk" :key="product.name">
                      <div style="max-width: 200px; max-height: 200px; flex-shrink: 0;">
                        <template v-if="product.seo?.slug && product.seo.slug.trim() !== ''">
                          <a :href="`https://rua11store-catalog-api.vercel.app/products/productView/${product.seo.slug}`"
                            target="_blank" rel="noopener noreferrer" style="display: block;">
                            <v-img :src="product.image_path" :alt="product.seo?.slug" width="150" height="150" contain
                              class="cursor-pointer" />

                          </a>
                        </template>
                      </div>
                    </template>
                  </div>
                </v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
        </div>
        <!-- Carousel Comentários -->
        <v-row justify="center" class="my-4">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-carousel cycle hide-delimiters :show-arrows="false" height="180" interval="7000"
              v-model="activeCommentIndex">
              <v-carousel-item v-for="(comment, index) in comments" :key="comment.id">
                <v-card outlined class="mx-auto pa-4" max-width="600" elevation="0">
                  <v-row align="center">
                    <v-col cols="3" class="text-center">
                      <v-avatar size="34">
                        <v-img :src="comment.avatar_url" alt="Avatar" />
                      </v-avatar>
                    </v-col>
                    <v-col cols="6">

                      <div style="font-style: italic; font-size: 14px; margin-top: 4px;">"{{ comment.comment }}"</div>
                      <div style="font-size: 10pxpx; color: gray; margin-top: 4px;">
                        <strong>{{ comment.user_name }}</strong> - {{ new Date(comment.created_at).toLocaleDateString()
                        }}
                      </div>
                    </v-col>
                  </v-row>
                </v-card>
              </v-carousel-item>
            </v-carousel>
          </v-col>
        </v-row>
      </div>

      
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
  comments?: Comment[]
}
interface Comment {
  id: number
  avatar_url: string
  comment: string
  created_at: string
  user_name: string
}


const productsData = ref<Product[]>([])
const comments = ref<Comment[]>([])
const activeIndex = ref(0)
const activeCommentIndex = ref(0)

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

    comments.value = []
    response.data.forEach((product: Product) => {
      if (product.comments) {
        comments.value.push(...product.comments)
      }
    })
  } catch (error) {
    console.error('Erro ao buscar produtos:', error)
  }
}


const chunkSize = 2
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

  setInterval(() => {
    const maxIndex = chunkedProducts.value.length - 1
    activeIndex.value = activeIndex.value >= maxIndex ? 0 : activeIndex.value + 1
  }, 5000)

  setInterval(() => {
    const maxCommentIndex = comments.value.length - 1
    activeCommentIndex.value = activeCommentIndex.value >= maxCommentIndex ? 0 : activeCommentIndex.value + 1
  }, 7000)
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
