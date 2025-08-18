<template>
  <v-container class="fill-height">
    <v-row justify="center" no-gutters>
      <v-col cols="12" sm="10" md="8" lg="6" xl="4">
        <v-card class="pa-4" elevation="0">
          <!-- Nome e preço -->
          <v-card-title class="text-h6 text-sm-h6 text-md-h6">

            {{ product.name }}

          </v-card-title>


          <v-card-subtitle class="text-subtitle-1 text-sm-h8 text-md-h8">
            R$ {{ product.price }}
          </v-card-subtitle>

          <!-- Carrossel de imagens -->
          <v-card-text>
            <v-row justify="center" no-gutters>
              <v-col cols="12" md="12" sm="10" xl="2">
                <v-defaults-provider :defaults="{ VBtn: { variant: 'outlined', color: '#eee' } }">
                  <v-sheet class="mx-auto overflow-hidden" rounded="xl">
                    <v-carousel v-model="currentIndex" progress="purple" show-arrows="hover" hide-delimiter
                      height="auto">
                      <!-- Primeira imagem: thumbnail -->
                      <v-carousel-item class="carousel-img" v-if="product.thumbnail_path" :src="product.thumbnail_path"
                        :alt="product?.seo?.slug">
                      </v-carousel-item>

                      <!-- Outras imagens -->
                      <v-carousel-item class="carousel-img" v-for="(img, index) in product.images" :key="index"
                        :src="img.url">
                      </v-carousel-item>
                    </v-carousel>

                    <!-- Overlay com legenda -->
                    <v-overlay :scrim="false"
                      content-class="d-flex flex-column align-center justify-space-between pointer-pass-through py-3"
                      contained model-value no-click-animation persistent>

                    </v-overlay>
                  </v-sheet>
                  <div class="text-center">
                    <v-chip :text="`${currentIndex + 1} / ${product.images.length + 1}`" color="deep-purple"
                      size="small" variant="flat"></v-chip>
                  </div>
                </v-defaults-provider>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-text>
            <p class="text-body-2 text-sm-body-1 text-center">{{ product.description }}</p>
          </v-card-text>


          <v-divider class="border-opacity-90" color="deep-purple" :thickness="2"></v-divider>

          <!-- Botões -->
          <v-card-actions class="d-flex flex-wrap justify-center" style="gap: 1px;">
            <v-btn color="success" @click="goToWhatsApp" variant="elevated" size="small" :block="$vuetify.display.xs">
              <v-icon left size="large">mdi-whatsapp</v-icon>
            </v-btn>

            <v-btn color="primary" href="https://rua11store-web.vercel.app/" size="small" variant="elevated"
              :block="$vuetify.display.xs">
              <v-icon left size="large">mdi-storefront</v-icon>
            </v-btn>

            <v-btn color="info" @click="downloadApp" variant="elevated" size="small" :block="$vuetify.display.xs">
              <v-icon left size="large">mdi-download</v-icon>
            </v-btn>
          </v-card-actions>

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

    goToWhatsApp() {
      const message = `Olá, tenho interesse no produto: ${this.product.name}`;
      const phone = "5511999999999"; // seu número aqui
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