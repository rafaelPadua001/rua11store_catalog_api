<template>
  <v-container class="fill-height">
    <v-row justify="center" no-gutters>
      <v-col cols="12" sm="10" md="8" lg="10" xl="6">
        <v-card class="pa-2">

          <!-- Nome e preço -->
          <v-card-title class="d-flex justify-start">
            <h3 style="font-size: 18px;">
              {{ product.name }}
            </h3>
          </v-card-title>

          <v-divider></v-divider>
          <v-card-subtitle class="text-h6">
            R$ {{ product.price }}
          </v-card-subtitle>

          <!-- Carrossel de imagens -->
          <v-card-text>
            <v-row justify="center" no-gutters>
              <v-col>
                <v-defaults-provider :defaults="{ VBtn: { variant: 'outlined', color: '#eee' } }">
                  <v-sheet class="mx-auto overflow-hidden" rounded="lg">
                    <v-carousel v-model="currentIndex"  progress="purple"
                      show-arrows="hover" hide-delimiter>
                      <!-- Primeira imagem: thumbnail -->
                      <v-carousel-item v-if="product.thumbnail_path" :src="product.thumbnail_path"
                        :alt="product?.seo?.slug">

                      </v-carousel-item>



                      <!-- Outras imagens -->
                      <v-carousel-item v-for="(img, index) in product.images" :key="index" :src="img.url">

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
            <p class="text-center">{{ product.description }}</p>
          </v-card-text>

          <v-divider></v-divider>

          <!-- Botões -->
          <v-card-actions class="d-flex flex-wrap justify-center" style="gap: 1px;">
            <v-btn color="success" @click="goToWhatsApp" variant="elevated" size="small">
              <v-icon left size="large">mdi-whatsapp</v-icon>
            </v-btn>

            <v-btn color="primary" href="https://rua11store-web.vercel.app/" size="small" variant="elevated">
              <v-icon left size="large">mdi-storefront</v-icon>
            </v-btn>

            <v-btn color="info" @click="downloadApp" variant="elevated" size="small">
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
import { shallowRef } from "vue";

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
