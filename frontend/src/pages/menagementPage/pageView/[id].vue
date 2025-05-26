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
const api = axios.create({
  baseURL: window.location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://rua11storecatalogapi-production.up.railway.app",
  headers: { "Content-Type": "application/json" },
});
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
  },
  methods: {
    stripHtml(html) {
      const div = document.createElement('div');
      div.innerHTML = html;
      return div.textContent || div.innerText || "";
    },
  }
};
</script>
