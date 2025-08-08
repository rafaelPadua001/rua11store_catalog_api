<template>
  <v-container class="fill-height">
    <v-row justify="center">
      <v-col cols="12" sm="12" md="8" lg="10" xl="6">
        <v-card class="pa-2">

          <!-- Imagem do produto -->
          <v-img
            :src="product.thumbnail_path"
            :alt="product?.seo?.slug"
            height="250"
            contain
            class="mb-4"
          ></v-img>

          <!-- Nome e preço -->
          <v-card-title class="d-flex justify-start">
            <h4 style="font-size: 14px;">
              {{ product.name }} - R$ {{ product.price }}
            </h4>
          </v-card-title>

          <!-- Descrição e palavras-chave -->
          <v-card-text class="text-justify">
            <div><p>{{ product.description }}</p></div>

            <div v-if="product?.seo?.meta_keywords">
              <v-chip-group column>
                <v-chip
                  v-for="(keyword, index) in product.seo.meta_keywords.split(',')"
                  :key="index"
                  class="ma-1"
                  color="primary"
                  text-color="white"
                  outlined
                  small
                >
                  {{ keyword.trim() }}
                </v-chip>
              </v-chip-group>
            </div>
          </v-card-text>

          <!-- Botões -->
          <v-card-actions
            class="d-flex flex-wrap justify-center mt-4"
            style="gap: 1px;"
          >
            <v-btn
              color="success"
              @click="goToWhatsApp"
              style="min-width: 180px;"
            >
              <v-icon left>mdi-whatsapp</v-icon>
              Pedir pelo WhatsApp
            </v-btn>

            <v-btn
              color="primary"
              href="https://rua11store-web.vercel.app/"
              style="min-width: 180px;"
            >
              <v-icon left>mdi-storefront</v-icon>
              Comprar na Loja
            </v-btn>

            <v-btn
              color="info"
              @click="downloadApp"
              style="min-width: 180px;"
            >
              <v-icon left>mdi-download</v-icon>
              Baixar App
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
