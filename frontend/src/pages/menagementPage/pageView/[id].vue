<!-- PageView.vue -->
<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div class="text-center" background>
        <h1 class="text-h3 font-weight-bold">{{ page.title }}</h1>
        <div class="text-body-2 font-weight-light mb-n1">{{ stripHtml(page.content) }}</div>
      </div>
    </v-responsive>
  </v-container>

</template>

<script>
import axios from "axios";
import { useSeo } from '../../../useSeo';


const api = axios.create({
  baseURL: window.location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

const { setSeo } = useSeo()
export default {
  data() {
    return {
      page: {}
    };
  },
  async created() {
    const pageId = this.$route.params.id;
    const response = await api.get(`/pages/pages/${pageId}`);
    this.page = response.data;
    this.loadComponentFromAPI();
  },
  methods: {
    stripHtml(html) {
      const div = document.createElement('div');
      div.innerHTML = html;
      return div.textContent || div.innerText || "";
    },
    async loadComponentFromAPI() {
      try {
        const pageName = this.page.title;
        const encodedPageName = encodeURIComponent(pageName);
        const response = await api.get(`/pages/pages/${encodedPageName}`);

        // pageTitle.value = response.data.title;
        // pageContent.value = response.data.content;
        // pageId = response.data.id;
        //loadFailed.value = false;

        await this.loadSeoFromAPI(response.data.id);

      } catch (error) {
        console.error('Erro ao buscar componente:', error);
        // loadFailed.value = true;
      }
    },
    async loadSeoFromAPI(pageId) {
      try {
        const response = await api.get(`/seo/seo/${pageId}`);
        const seoData = response.data.seo;

        setSeo(seoData);  // atualiza SEO via composable
      } catch (error) {
        console.error('Erro ao buscar SEO:', error);
      }
    }
  }
};
</script>
