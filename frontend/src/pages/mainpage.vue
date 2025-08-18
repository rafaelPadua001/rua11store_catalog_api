<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height ms-0 me-auto" max-width="100%">
      <div v-if="!loadFailed && pageContent" class="px-2 px-sm-4 align-center">

        <!-- HERO -->
        <v-row justify="center" class="my-0">
          <v-col>
            <v-card elevation="4" :color="pageBackgroundColor" class="rounded-lg overflow-hidden hero-card"
              v-if="pageBackgroundColor || pageImage">
              <v-img :src="pageImage" :alt="pageTitle" max-height="320" height="100%" class="mx-auto d-block" />
              <v-card-text class="py-0 text-center">
                <div class="text-h6 text-sm-h4 font-weight-bold">
                  {{ pageHeroTitle }}
                </div>
                <div class="text-body-2 text-sm-body-1">
                  {{ pageHeroSubTitle }}
                </div>
              </v-card-text>

              <!-- Botões Hero -->
              <v-card-text v-if="pageHeroButtons && pageHeroButtons.length >= 1"
                class="d-flex justify-center flex-wrap gap-2 py-0">
                <v-row justify="center" no-gutters>
                  <v-col v-for="(button, index) in pageHeroButtons" :key="index">

                    <v-btn class="mx-0 text-caption hover-btn" size="x-large" target="_blank" block
                      :color="button.heroButtonBackgroundColor" :href="button.url" variant="elevated">
                      <v-icon :icon="button.icon.value" class="mr-1" size="large"></v-icon>
                      {{ button.label }}
                    </v-btn>


                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Produtos -->
        <div class="mt-14 d-flex justify-center flex-wrap">
          <v-row justify="center" class="my-2">
            <v-col cols="12" sm="12" md="10" lg="6">
              <v-carousel :show-arrows="false" cycle hide-delimiters max-width="100%" interval="750000"
                v-model="activeIndex">
                <v-carousel-item v-for="(chunk, index) in chunkedProducts" :key="index">
                  <v-row justify="center" class="pa-2" dense>
                    <v-col v-for="product in chunk" :key="product.name" cols="12" sm="6" md="6">
                      <template v-if="product.seo?.slug && product.seo.slug.trim() !== ''">
                        <v-card elevation="0">
                          <v-card-text>
                            <a :href="`https://rua11store-catalog-api.vercel.app/products/productView/${product.seo.slug}`"
                              target="_blank" rel="noopener noreferrer">

                              <v-img :src="product.thumbnail_path" :alt="product.seo?.slug" class="cursor-pointer"
                                cover>
                                <v-chip class="ma-0" color="primary" text-color="white"
                                  style="position: absolute; top: 0; right: 0;">
                                  <strong>R$ {{ product.price ?? '0,00' }}</strong>
                                </v-chip>
                              </v-img>
                            </a>
                          </v-card-text>

                        </v-card>
                      </template>
                    </v-col>
                  </v-row>
                </v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
        </div>

        <!-- Carousel Comentários -->
        <h3 class="text-center">Testimonials</h3>
        <v-divider></v-divider>
        <div class="d-flex justify-center flex-wrap">
          <v-row justify="center">
            <v-col cols="12" sm="10" md="8" lg="6">
              <v-carousel cycle hide-delimiters :show-arrows="false" interval="7000" v-model="activeCommentIndex">
                <v-carousel-item v-for="(comment, index) in comments" :key="comment.id">
                  <v-card v-if="comment.status === 'ativo'" class="mx-auto pa-8" max-width="100%" elevation="0">
                    <v-row no-gutters class="align-center">
                      <v-col cols="auto" class="pr-4">
                        <v-avatar size="60">
                          <v-img :src="comment.avatar_url" alt="Avatar" />
                        </v-avatar>
                      </v-col>
                      <v-col>
                        <div style="font-style: italic; font-size: 16px; margin-top: 4px; color: gray;">
                          <p>
                            "{{ comment.comment }}" -
                            <strong style="font-size: 12px; color: black">
                              {{ comment.user_name }}
                            </strong>
                          </p>
                        </div>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
        </div>
      </div>

      <!-- Loader -->
      <div v-else class="text-center pa-4">
        <v-progress-circular indeterminate color="primary" size="64" />
        <p v-if="slowServer" class="mt-2 text-grey">
          Nosso servidor está iniciando... isso pode levar alguns segundos.
        </p>
        <p v-else class="mt-2 text-grey">Carregando dados...</p>
      </div>
    </v-responsive>

    <!-- WhatsApp -->
    <v-btn color="deep-purple" dark class="whatsapp-btn" href="https://wa.me/556191865680" target="_blank"
      elevation="10" icon>
      <v-icon size="28">mdi-whatsapp</v-icon>
    </v-btn>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import axios from 'axios'
import { useSeo } from '../useSeo'
import { useRoute } from 'vue-router'

const route = useRoute()
const slug = (route.params as any).slug

const loadFailed = ref(false)
const pageTitle = ref('')
const pageContent = ref('')
const pageHeroTitle = ref('')
const pageHeroSubTitle = ref('')
const pageBackgroundColor = ref('')
const pageImage = ref('')
const pageHeroButtons = ref<any[]>([])
const slowServer = ref(false)

interface Product {
  name: string
  thumbnail_path: string
  price: number
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
  status: string
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
    let pageId: number | undefined
    const slug = (route.params as { slug?: string }).slug

    if (slug) {
      const productResponse = await api.get(`/products/by-slug/${slug}`)
      pageTitle.value = productResponse.data.title
      pageContent.value = productResponse.data.description
      pageId = productResponse.data.id
    } else {
      const pageName = 'Home Page'
      const encodedPageName = encodeURIComponent(pageName)
      const pageResponse = await api.get(`/pages/pages/${encodedPageName}`)
      pageTitle.value = pageResponse.data.title
      pageContent.value = pageResponse.data.content
      pageHeroTitle.value = pageResponse.data.hero_title
      pageHeroSubTitle.value = pageResponse.data.hero_subtitle
      pageBackgroundColor.value = pageResponse.data.hero_background_color
      pageImage.value = pageResponse.data.hero_image
      pageHeroButtons.value = pageResponse.data.hero_buttons
      pageId = pageResponse.data.id
    }

    loadFailed.value = false

    if (pageId) {
      await loadSeoFromAPI(pageId)
    }
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

const { smAndDown } = useDisplay()
const chunkSize = computed(() => (smAndDown.value ? 1 : 2))

const chunkedProducts = computed(() => {
  const chunks = []
  for (let i = 0; i < productsData.value.length; i += chunkSize.value) {
    chunks.push(productsData.value.slice(i, i + chunkSize.value))
  }
  return chunks
})

onMounted(() => {
  setTimeout(() => {
    if (!pageContent.value) {
      slowServer.value = true
      loadComponentFromAPI()
      loadProductsToCarousel()
    }
  }, 5000)

  loadComponentFromAPI()
  loadProductsToCarousel()

  setInterval(() => {
    const maxIndex = chunkedProducts.value.length - 1
    activeIndex.value = activeIndex.value >= maxIndex ? 0 : activeIndex.value + 1
  }, 5000)

  setInterval(() => {
    const maxCommentIndex = comments.value.length - 1
    activeCommentIndex.value =
      activeCommentIndex.value >= maxCommentIndex ? 0 : activeCommentIndex.value + 1
  }, 7000)
})
</script>

<style scoped>
.hero-card{
  height: 49vh;
  margin: 0;
  justify-content: center; 
  align-items: center;
  background-color: #4b00b5; /* Roxo base */
  background-image: radial-gradient(circle at center, rgba(255,255,255,0.1) 1px, transparent 1px),
    repeating-radial-gradient(circle at center, rgba(255,255,255,0.05), rgba(255,255,255,0.05) 10px, transparent 10px, transparent 20px),
    repeating-conic-gradient(rgba(255,255,255,0.05) 0deg 5deg, transparent 5deg 10deg);
   background-size: cover;
}
.v-btn {
  margin-left: 1px !important;
  margin-right: 1px !important;
}

.hover-btn {
  transition: transform 0.2s, box-shadow 0.2s;
  /* animação suave */
}

.hover-btn:hover {
  transform: translateY(-3px);
  /* leve "subida" do botão */
  box-shadow: 0px 8px 25px rgba(92, 92, 92, 0.3);
  /* sombra maior no hover */
  opacity: 0.90
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
