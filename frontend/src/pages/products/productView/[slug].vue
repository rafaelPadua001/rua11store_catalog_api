<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="6">
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
      <v-col cols="6">
        <v-row>
          <v-col cols="12" sm="12">
            <span class="text-h4">{{ product.name }}</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <span class="text-h5">R$ {{ product.price }}</span>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <div style="display: flex; gap: 8px;">
              <v-btn color="black" @click="addItemCart(product)">Adicionar ao carrinho</v-btn>
              <v-btn color="success">Whatsapp Button</v-btn>
            </div>
          </v-col>
        </v-row>


      </v-col>

    </v-row>
    <!-- Sugestoes de produtos -->
    <v-row>
      <v-col cols="12">
        <v-card>
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
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            Descrição
          </v-card-title>
          <v-card-text>
            <v-card-text>
              <p class="text-body-2 text-sm-body-2 text-justify">{{ product.description }}</p>
            </v-card-text>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
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
        if (product.product_quantity == 0) {
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
      } catch (e) {
        console.log("erro ao inserir item no carrinho", e);
      }
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
  },
};
</script>
<style>
.carousel-img {
  object-fit: contain;
}
</style>