<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height ms-0 me-auto" max-width="100%">
      <div v-if="!loadFailed && pageContent" class="px-2 px-sm-10 align-center">
        <!-- HERO -->
        <v-row justify="center" class="my-0">
          <v-col>
            <v-card elevation="4" :color="pageBackgroundColor" class="rounded-xl overflow-hidden hero-card"
              v-if="pageBackgroundColor || pageImage">
              <v-row no-gutters align="center">
                <v-col v-if="pageHeroTitle || pageHeroSubTitle" cols="12" md="6" class="px-4">
                  <v-card-text class="py-0 text-center">
                    <div class="text-h6 text-sm-h2 font-weight-bold">
                      {{ pageHeroTitle }}
                    </div>
                    <div class="text-body-2 text-sm-body-1">
                      {{ pageHeroSubTitle }}
                    </div>
                  </v-card-text>
                </v-col>


                <v-col cols="12" md="6">
                  <v-img :src="pageImage" :alt="pageTitle" max-height="450" class="mx-auto d-block" />
                </v-col>

              </v-row>

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
        <br></br>
        <br></br>
        <!-- Produtos -->
        <div>
          <v-row justify="center">
                    <v-col cols="6" md="4" sm="4" v-for="product in productsData" :key="product.name" elevation="2">
                      <v-row>
                        <v-col>
                           <v-card class="d-flex flex-column" >
                        <v-card-text>
                         
                          <template v-if="product.seo?.slug && product.seo.slug.trim() !== ''">
                              <a :href="`https://rua11store-catalog-api.vercel.app/products/productView/${product.seo.slug}`"
                                  target="_blank" rel="noopener noreferrer">
                                  <v-img :src="product.thumbnail_path" :alt="product.seo?.slug" class="cursor-pointer"
                                    contain >
                                    
                                    <v-chip class="ma-0" color="deep-purple" text-color="white"
                                      style="position: absolute; top: 0; right: 0;">
                                      <strong>R$ {{ product.price ?? '0,00' }}</strong>
                                    </v-chip>
                                    
                                  </v-img>
                                  <v-chip class="ma-0" v-if="product.product_quantity == 0" color="error">Esgotado</v-chip>
                                </a>

                              <!--<v-card-text class="text-center">
                            <v-btn color="primary">Comprar</v-btn>
                          </v-card-text> -->

                          
                            <span class="d-block text-truncate " style="max-width: 100%; overflow: hidden;">
                              <strong>{{ product.name }}</strong>
                            </span>

                          </template>
                         
                        </v-card-text>

                        <v-card-actions class="d-flex justify-center align-center">
                        
                          <v-btn icon color="primary" @click="addItemCart(product)">
                            <v-icon>mdi-cart-plus</v-icon>
                          </v-btn>
                          
                       
                        </v-card-actions>
                          
                        </v-card>
                         <br></br>
                        </v-col>
                      </v-row>
                     
                     <v-spacer></v-spacer>
                  
                    </v-col>
                    
                  </v-row>
                 
        </div>

        <!--<div>
          <v-card class="rounded-xl overflow-hidden hero-card" elevation="4" width="100%" color="#b48a17">
            <v-card-title>Conheça nossos produtos !</v-card-title>
            <v-divider class="border-opacity-50" thickness="2" color="deep-purple"></v-divider>

            <v-card-text>
              <v-row justify="center" class="my-1">
                <v-col cols="auto" md="12" sm="12">
                  <v-carousel :show-arrows="false" cycle hide-delimiters max-width="100%" height="300" interval="750000"
                    v-model="activeIndex" max-height="100%">
                    <v-carousel-item v-for="(chunk, index) in chunkedProducts" :key="index">
                      <v-row justify="center">
                        <v-col cols="12" sm="4" md="4" v-for="product in chunk" :key="product.name">
                          <template v-if="product.seo?.slug && product.seo.slug.trim() !== ''">
                            <v-card class="pa-2 align-center rounded-lg overflow-hidden" elevation="0"
                              style="background-color: rgba(255, 255, 255, 0.1);">
                              <v-card-text>
                                <a :href="`https://rua11store-catalog-api.vercel.app/products/productView/${product.seo.slug}`"
                                  target="_blank" rel="noopener noreferrer">
                                  <v-img :src="product.thumbnail_path" :alt="product.seo?.slug" class="cursor-pointer"
                                    contain max-height="170">
                                    <v-chip class="ma-0" color="deep-purple" text-color="white"
                                      style="position: absolute; bottom: 0; right: 0;">
                                      <strong>R$ {{ product.price ?? '0,00' }}</strong>
                                    </v-chip>
                                  </v-img>
                                </a>


                              </v-card-text>

                            </v-card>
                            <span class="d-block text-truncate " style="max-width: 100%; overflow: hidden;">
                              <strong>{{ product.name }}</strong>
                            </span>

                          </template>

                        </v-col>
                      </v-row>
                    </v-carousel-item>
                  </v-carousel>
                </v-col>
              </v-row>
            </v-card-text>
            <v-divider class="border-opacity-50" thickness="2" color="deep-purple"></v-divider>
            <v-card-actions>
              <v-btn block href="https://rua11store-web.vercel.app/" target="_blank" icon>
                <!--<v-icon>mdi-eye</v-icon>
                <span>Ver tudo</span>
              </v-btn>
            </v-card-actions>
          </v-card>

        </div>-->
        <br></br>
        <br></br>



        <div>
          <v-row no-gutters>
            <v-col>
              <v-card class="overflow-hidden" elevation="4" max-height="100%" color="trasparent">
                <v-card-title class="text-left white--text">
                  <span class="d-block title-responsive">
                    Por que escolher a Rua11Store ?
                  </span>
                </v-card-title>
                <v-divider class="border-opacity-20" thickness="2" color="grey"></v-divider>
                <v-card-text>
                  <v-row justify="center" align="center" class="text-center" no-gutters>
                    <v-col cols="12" sm="6" md="3" class="mb-4">
                      <span><v-icon size="x-large" class="mb-2 white--text"
                          color="primary">mdi-truck-fast</v-icon></span>
                      <div class="white--text font-weight-medium">Entrega rápida e segura</div>
                    </v-col>
                    <v-col cols="12" sm="6" md="3" class="mb-4">
                      <v-icon size="x-large" class="mb-2 white--text" color="success">mdi-lock-check</v-icon>
                      <div class="white--text font-weight-medium">Pagamento Seguro</div>
                    </v-col>
                    <v-col cols="12" sm="6" md="3" class="mb-4">
                      <v-icon size="x-large" class="mb-2 white--text" color="primary">mdi-thumb-up</v-icon>
                      <div class="white--text font-weight-medium">Qualidade Garantida</div>
                    </v-col>

                    <v-col cols="12" sm="6" md="3" class="mb-4">
                      <v-icon size="x-large" class="mb-2 white--text" color="deep-purple">mdi-gift-open</v-icon>
                      <div class="white--text font-weight-medium">Promoções exclusivas</div>
                    </v-col>
                  </v-row>
                </v-card-text>

              </v-card>
            </v-col>
          </v-row>
        </div>
        <br></br>
        <br></br>

        <div>
          <v-row no-gutters>
            <v-col>
              <v-card class="rounded-xl overflow-hidden hero-card" elevation="4" max-height="275" color="grey">
                <v-card-title class="text-left white--text">
                  <span class="d-block title-responsive">O que nossos clientes estão dizendo:</span></v-card-title>
                <v-card-text>

                  <v-divider></v-divider>
                  <br></br>


                  <div class="d-flex justify-center flex-wrap">
                    <v-row no-gutters>
                      <v-col cols="12">
                        <v-carousel cycle hide-delimiters :show-arrows="false" interval="7000"
                          v-model="activeCommentIndex">
                          <v-carousel-item v-for="(pair, pairIndex) in chunkedComments" :key="pairIndex">
                            <v-row>
                              <v-col v-for="(comment, index) in pair" :key="comment.id" cols="auto" md="6" class="mb-2">
                                <v-card v-if="comment.status === 'ativo'" class="mx-auto pa-8" elevation="1"
                                  style="background-color: rgba(255, 255, 255, 0.7);">
                                  <v-row class="align-center" no-gutters>
                                    <v-col cols="auto" class="pr-8">
                                      <v-avatar size="60">
                                        <v-img :src="comment.avatar_url" alt="Avatar" />
                                      </v-avatar>
                                    </v-col>
                                    <v-col>
                                      <div style="font-style: italic; font-size: 14px; margin-top: 4px; color: gray;">
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
                              </v-col>
                            </v-row>
                          </v-carousel-item>
                        </v-carousel>
                      </v-col>
                    </v-row>
                  </div>
                </v-card-text>
              </v-card>
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

    <!-- FAB Customizado -->
    <div class="fab-container">
      <!-- Botão principal -->
      <button class="fab-main" @click="fab = !fab">
        <v-icon>mdi-chat</v-icon>
      </button>

      <!-- Botões filhos -->
      <transition-group name="fab" tag="div">
        <a v-for="btn in fabButtons" :key="btn.key" v-show="fab" :href="btn.href" target="_blank" class="fab-child"
          :style="{ backgroundColor: btn.color }">
          <v-icon>{{ btn.icon }}</v-icon>
        </a>
      </transition-group>
    </div>
  </v-container>

  <!-- Coupons window: fora do container -->

  <transition name="slide-up-enter-from" v-if="coupon && showNotify">
    <v-sheet elevation="12" rounded="lg" max-width="400" width="100%"
      style="position: fixed; bottom: 150px; right: 20px; z-index: 9999; overflow: hidden; height: 350px;">
      <!-- Imagem de fundo -->
      <v-img :src="`${coupon.image_path}`" cover class="absolute inset-2" style="z-index: 0;">

        <template #placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center" style="background-color: rgba(0,0,0,0.05);">
            <v-progress-circular indeterminate color="deep-purple accent-4"></v-progress-circular>
          </v-row>
        </template>

        <!-- Caso haja erro ao carregar a imagem -->
        <template #error>
          <v-row class="fill-height ma-0" align="center" justify="center" style="background-color: rgba(255,0,0,0.1);">
            <span class="text-center">Imagem não disponível</span>
          </v-row>
        </template>
      </v-img>

      <!-- Overlay semitransparente -->
      <div style="position: absolute; inset: 0; background-color: rgba(0,0,0,0.5); z-index: 0;"></div>

      <!-- Conteúdo do cupom sobre a imagem -->
      <div
        style="position: absolute; inset: 0; z-index: 2; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; text-align: center; padding: 16px;">
        <v-icon class="mb-2" color="yellow" size="50" icon="mdi-gift"></v-icon>
        <h3 class="mb-2 font-weight-bold">🎉 Cupom Especial!</h3>
        <p class="mb-4">Use o cupom <b>{{ coupon.code }}</b> e ganhe <b>{{ coupon.discount }}% OFF</b>!</p>

        <div class="d-flex justify-end w-100">
          <v-btn color="deep-purple-accent-4" variant="flat" rounded @click="copyCoupon(coupon.code)">
            Copiar
          </v-btn>
          <v-btn color="success" variant="flat" rounded class="ml-2" @click="showNotify = false">
            Fechar
          </v-btn>
        </div>
      </div>
    </v-sheet>
  </transition>




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
const coupon = ref<any | null>(null)
const showNotify = ref(false)
const pageTitle = ref('')
const pageContent = ref('')
const pageHeroTitle = ref('')
const pageHeroSubTitle = ref('')
const pageBackgroundColor = ref('')
const pageImage = ref('')
const pageHeroButtons = ref<any[]>([])
const slowServer = ref(false)
const fab = ref(false)
const fabButtons = [
  {
    key: 'wa',
    icon: 'mdi-whatsapp',
    color: 'green',
    href: 'https://wa.me/556191865680'
  },
  {
    key: 'msg',
    icon: 'mdi-comment-text',
    color: 'teal',
    href: 'https://wa.me/556191865680?text=Ol%C3%A1%2C%20quero%20mais%20informa%C3%A7%C3%B5es!'
  },
  {
    key: 'group',
    icon: 'mdi-account-group',
    color: 'blue',
    href: 'https://chat.whatsapp.com/XXXXXXXXXXXXXXX'
  }
]

interface Product {
  id: number,
  name: string
  thumbnail_path: string
  price: number
  product_quantity: number,
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
interface Coupons {
  id: number
  title: string
  code: string
  discount: string
  end_date: string
  image_path: string
  client_id: string
}

const productsData = ref<Product[]>([])
const comments = ref<Comment[]>([])
let coupons = ref<Coupons[]>([])
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
      pageHeroButtons.value = Array.isArray(pageResponse.data.hero_buttons)
        ? pageResponse.data.hero_buttons
        : JSON.parse(pageResponse.data.hero_buttons || "[]")

      pageId = pageResponse.data.id
    }

    loadFailed.value = false

    if (pageId) {
      await loadSeoFromAPI(pageId);
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
    return false;
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

async function loadCoupons() {
  try {
    const response = await api.get('coupon/promotional_coupons')
    let coupons = response.data

    if (coupons.length > 0) {
      coupon.value = coupons[Math.floor(Math.random() * coupons.length)]
      // showNotify.value = true
    }

  }
  catch (error) {
    console.log('erro ao buscar cupons:', error);
  }
}

const { smAndDown } = useDisplay()
const chunkSize = computed(() => (smAndDown.value ? 1 : 3))

const chunkedProducts = computed(() => {
  const chunks = []
  for (let i = 0; i < productsData.value.length; i += chunkSize.value) {
    chunks.push(productsData.value.slice(i, i + chunkSize.value))
  }
  return chunks
})

const chunkedComments = computed(() => {
  const size = smAndDown.value ? 1 : 4
  const chunks: Comment[][] = []
  for (let i = 0; i < comments.value.length; i++) {
    chunks.push(comments.value.slice(i, i + size))
  }

  return chunks
})

function copyCoupon(code: string) {
  navigator.clipboard.writeText(code)
  alert(`Coupon ${code} copiado!`)
}

function handleScroll() {
  const bottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 10
  if (bottom) {
    showNotify.value = true
    window.removeEventListener("scroll", handleScroll)
  }
}

const addItemCart = async (product: Product) => {
  try{
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');
    if(product.product_quantity == 0){
      alert("Protudo sem estoque");
    }
    
    const response = await api.post(`/cart/add-cart`, {
      product_id: product.id,
      quantity: 1
    },
    {
       headers: {
        Authorization: `Bearer ${token}`
      }
    });
    console.log('Item adicionado');
  }catch(e){
    console.log("erro ao inserir item no carrinho", e);
  }
}

onMounted(() => {
  window.addEventListener("scroll", handleScroll)
})

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll)
})

onMounted(() => {
  setTimeout(() => {
    if (!pageContent.value) {
      slowServer.value = true
      loadComponentFromAPI()
      loadProductsToCarousel()
      loadCoupons()
    }
  }, 5000)

  loadComponentFromAPI()
  loadProductsToCarousel()
  loadCoupons()

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
.hero-card {
  background-image:
    radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    repeating-radial-gradient(circle at center, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.09) 1px, transparent 1px, transparent 2px),
    repeating-conic-gradient(rgba(255, 255, 255, 0.05) 0deg 4deg, transparent 0deg 10deg);
  background-size: cover;
  color: white;
  min-height: 375px;
  /* garante espaço suficiente para botões */
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

.fab-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  gap: 12px;
  z-index: 9999;
}

.fab-main {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #673ab7;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.fab-child {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.fab-enter-active,
.fab-leave-active {
  transition: all 0.2s;
}

.fab-enter-from,
.fab-leave-to {
  opacity: 0;
  transform: translateY(20px);
}


.mx-auto.text-center {
  max-width: 100%;
  padding-left: 10px;
  padding-right: 10px;
}

.title-responsive {
  font-weight: bold;
  font-size: 1.2rem;
  /* desktop */
  line-height: 1.2;
}

/* Animação personalizada */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

@media (max-width: 960px) {
  .title-responsive {
    font-size: 1.2rem;
    /* tablet */
  }
}

@media (max-width: 600px) {
  .title-responsive {
    font-size: 1.0rem;
    /* mobile */
    word-break: break-word;
    /* garante quebra de linha */
  }
}

@media (max-width: 600px) {
  .floating-coupon {
    max-width: 90%;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
