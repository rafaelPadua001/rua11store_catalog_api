<template>
  <v-container>
    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="6">
        <v-defaults-provider :defaults="{ VBtn: { variant: 'outlined', color: '#eee' } }">
          <v-sheet class="mx-auto overflow-hidden" rounded="xl">
            <v-carousel v-model="currentIndex" class="mx-auto" progress="purple" show-arrows="hover" hide-delimiter
              height="auto">
              <!-- Primeira imagem: thumbnail -->
              <v-carousel-item class="carousel-img" v-if="product.thumbnail_path" :src="product.thumbnail_path"
                :alt="product?.seo?.slug">
                <v-chip class="ma-2" v-if="product.product_quantity == 0" color="error">Esgotado</v-chip>
              </v-carousel-item>

              <!-- Outras imagens -->
              <v-carousel-item class="carousel-img" v-for="(img, index) in product.images" :key="index" :src="img.url">

              </v-carousel-item>
            </v-carousel>

            <!-- Overlay com legenda -->
            <v-overlay :scrim="false"
              content-class="d-flex flex-column align-center justify-space-between pointer-pass-through py-3" contained
              model-value no-click-animation persistent>

            </v-overlay>
          </v-sheet>
          <div class="text-center">
            <v-chip :text="`${currentIndex + 1} / ${product.images.length + 1}`" color="deep-purple" size="small"
              variant="flat"></v-chip>
          </div>
        </v-defaults-provider>
      </v-col>
      <v-col cols="12" md="6" class="px-4">
        <div class="text-center text-md-start">
          <span class="text-h3 text-sm-h4 font-weight-bold">
            {{ product.name }}
          </span>
        </div>
        <div class="text-center text-md-start mt-2">
          <span class="text-h6 text-md-h5">
            R$ {{ product.price }}
          </span>
        </div>

        <div class="d-flex flex-column flex-sm-row align-center justify-center justify-md-start mt-4"
          style="gap: 10px;">
          <v-btn color="black" @click="addItemCart(product)">
            <v-icon size="x-large">mdi-cart-plus</v-icon>
            Adicionar ao carrinho
          </v-btn>
          <v-btn color="success" @click="goToWhatsApp">
            <v-icon size="x-large">mdi-whatsapp</v-icon>
            Pedir pelo Whatsapp
          </v-btn>
        </div>




      </v-col>

    </v-row>
    <!-- Sugestoes de produtos -->
    <v-row>
      <v-col cols="12">
        <!--  <v-card>
          <v-toolbar color="transparent">
            <v-toolbar-title>
              <span class="text-h8">Combine com...</span>
            </v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-card>
              produtos
            </v-card>
            <v-card>
              produtos
            </v-card>
            <v-card>
              produtos
            </v-card>
            <v-card>
              produtos
            </v-card>
          </v-card-text>
        </v-card>-->
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12">
        <v-card elevation="2" rounded="lg">
          <v-card-title>
            Descrição
          </v-card-title>
          <v-card-text>
            <v-card-text>
              <p class="text-body-2 text-md-body-1 text-justify">{{ product.description }}</p>
            </v-card-text>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12">
        <v-card elevation="0">
          <v-card-title>
            Comments
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <v-row no-gutters>
              <v-col cols="3" md="1">
                <v-avatar color="grey" rounded="10" size="75">
                  <v-img height="100%" src="https://cdn.vuetifyjs.com/images/cards/server-room.jpg" contain></v-img>
                </v-avatar>
              </v-col>
              <v-col cols="6" md="3">
                <v-list-item class="" subtitle="Network engineer" title="Marcos Obrien">

                </v-list-item>
              </v-col>

              <v-col cols="12">
                <div class="d-flex align-end">
                  <v-textarea placeholder="Comment here..." rows="2" auto-grow class="flex-grow- mr-1">
                  </v-textarea>


                </div>

              </v-col>


            </v-row>
            <v-row no-gutters>
              <v-col cols="12">
                <div class="d-flex justify-end">
                  <v-btn color="primary" @click="submitComment()">Comment</v-btn>
                </div>

              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text>
            Load comments here....
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <transition name="fade">
      <v-alert v-if="alert" class="notification" type="success" variant="elevated" elevation="8" border="start"
        :text="alertMessage" title="Produto adicionado ao carrinho" />
      <v-alert v-else-if="alertError" class="notification" type="error" elevation="8" border="start"
        :text="alertMessage" title="Erro ao adicionar o produto ao carrinho">

      </v-alert>
    </transition>
  </v-container>
</template>

<script>
import axios from "axios";
import { useSeo } from "@/useSeo";


const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

export default {
  data() {
    return {
      product: { images: [] },
      currentIndex: 0,
      alert: null,
      alertError: null,
      alertMessage: '',
    };
  },
  async created() {
    await this.loadProduct();
  },
  computed: {
    currentImage() {
      // primeira é thumbnail, depois imagens
      if (this.currentIndex === 0) {
        return { url: this.product.thumbnail_path, label: this.product.name };
      }
      return this.product.images[this.currentIndex - 1] || null;
    },
  },
  watch: {
    "$route.params.slug": {
      immediate: false,
      handler: async function (newSlug, oldSlug) {
        if (newSlug !== oldSlug) {
          await this.loadProduct();
        }
      },
    },
  },
  methods: {
    async loadProduct() {
      const pageSlug = this.$route.params.slug;
      try {
        const response = await api.get(`/products/product/${pageSlug}`);
        this.product = response.data;

        if (this.product.seo) {
          const { setSeo } = useSeo();
          setSeo(this.product);
        }
      } catch (error) {
        console.error("Erro ao buscar produto:", error);
      }
    },
    async addItemCart(product) {
      try {
        const token = localStorage.getItem('token') || localStorage.getItem('access_token');
        if (!token) {
          return alert('Você precisa estar logado...');
        }

        if (product.product_quantity == 0) {
          // console.log(this.alert);
          this.showNotification();
          return;
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
        this.showNotification()
        console.log('Item adicionado');
      } catch (e) {
        console.log("erro ao inserir item no carrinho", e);
        this.notification();
      }
    },
    showNotification() {
      if (this.product.product_quantity === 0) {
        this.alertMessage = "Produto sem estoque";
        this.alertError = true;
        setTimeout(() => {
          this.alertError = false
        }, 3000);
        return;
      }
      this.alertMessage = `Produto ${this.product.name} - R$ ${this.product.price} adicionado ao carrinho`;
      this.alert = true;
      setTimeout(() => {
        this.alert = false;
      }, 3000); //desaparece em 3 segundos;

    },
    goToWhatsApp() {
      const message = `Olá, tenho interesse no produto: ${this.product.name}`;
      const phone = "556191865680"; // seu número aqui
      window.open(
        `https://wa.me/${phone}?text=${encodeURIComponent(message)}`,
        "_blank"
      );
    },

    downloadApp() {
      window.open(
        "https://play.google.com/store/apps/details?id=sua.app",
        "_blank"
      );
    },
    submitComment(){
      window.alert('Desculpe o transtorno. Isso ainda esta em desenvolvimento');
    }
  },
};
</script>
<style scoped>
.carousel-img {
  object-fit: cover;
  width: 100%;
  height: auto;

}

@media (max-width: 650px) {
  .carousel-img {
    max-height: 500px;
  }
}

.v-btn {
  font-size: 0.9rem;
  padding: 8px 12px;
}

.notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 350px;
  z-index: 9999;
}

/*anima notificação */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s, transform 0.4s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20);
}
</style>