<template>
  <v-row justify="center">
    <v-col cols="12" sm="12" md="10" lg="10" xl="6">
      <v-card class="pa-4">
        <!-- Título do produto -->


        <!-- Imagem do produto -->
        <v-img :src="product.image_url" :alt="product?.seo?.slug" height="300" contain class="mb-4"></v-img>
        <v-card-title>
          <h3>{{ product.name }} - R$ {{ product.price }}</h3>
        </v-card-title>

        <!-- Conteúdo do produto -->
        <v-card-text>
          <div>{{ product.description }}</div>
          <div v-if="product?.seo?.meta_keywords">
            <v-chip-group column>
              <v-chip v-for="(keyword, index) in product.seo.meta_keywords.split(',')" :key="index" class="ma-1"
                color="primary" text-color="white" outlined small>
                {{ keyword.trim() }}
              </v-chip>
            </v-chip-group>
          </div>

          <!-- <div v-if="product?.seo?.slug"><strong>Slug:</strong> {{ product.seo.slug }}</div> -->


        </v-card-text>

        <v-card-actions class="d-flex justify-center mt-4">
          <v-btn color="success" @click="goToWhatsApp" class="mx-2">
            <v-icon left>mdi-whatsapp</v-icon>
            Pedir pelo WhatsApp
          </v-btn>

          <v-btn color="primary" @click="goToStore" class="mx-2">
            <v-icon left>mdi-storefront</v-icon>
            Comprar na Loja
          </v-btn>

          <v-btn color="info" @click="downloadApp" class="mx-2">
            <v-icon left>mdi-download</v-icon>
            Baixar App
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
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