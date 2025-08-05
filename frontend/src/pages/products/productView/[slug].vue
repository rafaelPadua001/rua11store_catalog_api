<template>
  <v-container class=" fill-height">
    <v-row justify="center">
    <v-col cols="12" sm="12" md="8" lg="10" xl="6">
      <v-card class="pa-2">
        <!-- Imagem do produto -->
        <v-img :src="product.thumbnail_path" :alt="product?.seo?.slug" height="250" contain class="mb-4"></v-img>

        <v-card-title class="d-flex justify-start">
          <h4 style="font-size: 14px;">{{ product.name }} - R$ {{ product.price }}</h4>
        </v-card-title>

        <!-- Conteúdo do produto -->
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

        <!-- Botões responsivos -->
        <v-card-actions class="d-flex flex-wrap justify-center mt-4" style="gap: 1px;">
          <v-btn
            color="success"
            @click="goToWhatsApp"
            class="ma-0"
            style="min-width: 180px; max-width: 100%;"
          >
            <v-icon left>mdi-whatsapp</v-icon>
            Pedir pelo WhatsApp
          </v-btn>

          <v-btn
            color="primary"
            class="ma-0"
            href="https://rua11store-web.vercel.app/"
            style="min-width: 180px; max-width: 100%;"
          >
            <v-icon left>mdi-storefront</v-icon>
            Comprar na Loja
          </v-btn>

          <v-btn
            color="info"
            @click="downloadApp"
            class="ma-0"
            style="min-width: 180px; max-width: 100%;"
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
  baseURL: window.location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});


const setSeo = useSeo;
export default {
  data() {
    return {
      product: {}
    };
  },
  async created() {
    await this.loadProduct();
  },
  watch: {
    '$route.params.slug': {
      immediate: false,
      handler: async function (newId, oldId) {
        if (newId !== oldId) {
          await this.loadPage();
        }
      }
    }
  },
  methods: {
    async loadProduct() {
      const pageSlug = this.$route.params.slug;
      console.log(pageSlug);
      try {
        const response = await api.get(`/products/product/${pageSlug}`);
        this.product = response.data;
        await this.loadComponentFromAPI();
      } catch (error) {
        console.log('Erro ao buscar página');
      }

    },
  }
}
</script>