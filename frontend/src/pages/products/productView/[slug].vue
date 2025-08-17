<template>
  <v-container class="fill-height">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="10" xl="6">
        <v-card class="pa-2">
          <!-- Imagem do produto -->


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

          <!-- <v-defaults-provider :defaults="{ VBtn: { variant: 'outlined', color: '#eee' } }">
            <v-sheet class="overflow-hidden" max-width="700" rounded="xl">
              <v-carousel
                v-model="currentIndex"
                direction="vertical"
                height="400"
                progress="red"
                vertical-arrows="left"
                vertical-delimiters="right"
                hide-delimiters-backgrund
              >
                <v-carousel-item
                  v-for="(img, index) in product.images"
                ></v-carousel-item>
              </v-carousel>
            </v-sheet>
          </v-defaults-provider> -->
          <v-img :src="product.thumbnail_path" :alt="product?.seo?.slug" max-height="500" contain>
<template v-slot:placeholder>
      <div class="d-flex align-center justify-center fill-height">
        <v-progress-circular
          color="grey-lighten-4"
          indeterminate
        ></v-progress-circular>
      </div>
    </template>
          </v-img>
          <!-- Descrição e palavras-chave -->
          <!--<v-card-text class="text-justify">
            <v-row v-if="product?.seo?.meta_keywords">
              <v-col v-for="(keyword, index) in product.seo.meta_keywords.split(',')" :key="index">
                <v-chip-group column>
                  <v-chip>
                    {{ keyword.trim() }}
                  </v-chip>
                </v-chip-group>
              </v-col>
            </v-row>





          </v-card-text>
          <v-divider></v-divider> -->

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
      product: {},
    };
  },
  async created() {
    await this.loadProduct();
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

        // Carregar SEO do produto
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
