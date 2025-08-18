<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto">
      <div class="text-center">
        <v-row justify="center" class="mt-0 mb-4" no-gutters>
          <v-col cols="12">
              <!--<v-card elevation="0">
                <v-card-title class="text-left">{{ page.name }}</v-card-title>
              </v-card>-->
              <v-divider></v-divider>
              <v-card elevation="4" :color="page.hero_background_color" width="100%"
                class="rounded-lg overflow-hidden hero-card" v-if="page.hero_background_color || page.heroImage">
              <v-img  :src="page.hero_image" :alt="page.title" max-height="320" height="100%" class="mx-auto d-block" />
              <v-card-text class="py-0" v-if="page.hero_title || page.hero_subtitle">
                <v-row justify="center" no-gutters>
                  <v-col cols="auto">
                    {{ page.hero_title }}
                  </v-col>
                </v-row no-gutters>
                <v-row justify="center" >
                  <v-col cols="auto">
                    {{ page.hero_subtitle }}
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-text v-if="page.hero_buttons && page.hero_buttons.length >= 1">
                <v-row justify='center' no-gutters>
                  <v-col v-for="(button, index) in page.hero_buttons" :key="index">
                   <v-btn class="mx-0 text-caption hover-btn" size="x-large" target="_blank" block
                      :color="button.heroButtonBackgroundColor" :href="button.url" variant="elevated">
                      <v-icon :icon="button.icon.value" class="mr-1" size="large"></v-icon>
                      {{ button.label }}
                    </v-btn>
                   
                  </v-col>
                </v-row>

              </v-card-text>

            </v-card>

          </v-col>
        </v-row>
        
        <div class="mt-0 mb-1 d-flex justify-center flex-wrap" v-if="page.carousel_image && page.carousel_image.length >= 1">
          <v-row justify="center" class="my-2">
            <v-col cols="12" sm="10" md="8" lg="6">
              <v-carousel :show-arrows="false" cycle hide-delimiters height="350" interval="5000" v-model="activeIndex">
                <v-carousel-item v-for="(img, index) in page.carousel_image" :key="index">
                  <v-card elevation="0">
                    <v-img :src="img" width="300" height="300" contain class="mx-auto" />
                  </v-card>
                </v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
        </div>

       
       <!-- {{ page.name }} -->
         <v-card v-if="page.content">
          <v-card-text>
             <v-card-title class="text-left">{{ page.name }}</v-card-title>
             <v-divider></v-divider>
            <div class="text-body-2 text-left font-weight-light mb-n1" v-html="page.content"></div>
          </v-card-text>
         </v-card>
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
      page: {
        carousel_image: [],
        hero_image: "",
        hero_title: "",
        hero_subtitle: "",
        title: "",
        content: ""
      },
      activeIndex: 0
    };
  },
  async created() {
    await this.loadPage();
  },
  watch: {
    '$route.params.id': {
      immediate: false,
      handler: async function (newId, oldId) {
        if (newId !== oldId) {
          await this.loadPage();
        }
      }
    }
  },
  methods: {
    async loadPage() {
      const pageId = this.$route.params.id;
      try {
        const response = await api.get(`/pages/pages/${pageId}`);
        // mantém reatividade
        Object.assign(this.page, response.data);
        await this.loadComponentFromAPI();
      } catch (error) {
        console.log('Erro ao buscar página', error);
      }
    },

    stripHtml(html) {
      const div = document.createElement('div');
      div.innerHTML = html;
      return div.textContent || div.innerText || "";
    },

    async loadComponentFromAPI() {
      try {
        const pageTitle = this.page.title;
        const encodedPageTitle = encodeURIComponent(pageTitle);
        const response = await api.get(`/pages/pages/${encodedPageTitle}`);
        await this.loadSeoFromAPI(response.data.id);
      } catch (error) {
        console.error('Erro ao buscar componente:', error);
      }
    },

    async loadSeoFromAPI(pageId) {
      try {
        const response = await api.get(`/seo/seo/${pageId}`);
        const seoData = response.data.seo;
        setSeo(seoData);
      } catch (error) {
        console.error('Erro ao buscar SEO:', error);
      }
    }
  }
};
</script>

<style scopped>
.hero-card{
  height: 51vh;
  margin: 0;
  justify-content: center; 
  align-items: center;
  background-color: #4b00b5; /* Roxo base */
  background-image: radial-gradient(circle at center, rgba(255,255,255,0.1) 1px, transparent 1px),
    repeating-radial-gradient(circle at center, rgba(255,255,255,0.05), rgba(255,255,255,0.05) 10px, transparent 10px, transparent 20px),
    repeating-conic-gradient(rgba(255,255,255,0.05) 0deg 5deg, transparent 5deg 10deg);
   background-size: cover;
}
.v-btn {
  margin-left: 1px !important;
  margin-right: 1px !important;
}

.hover-btn {
  transition: transform 0.2s, box-shadow 0.2s;
  /* animação suave */
}

.hover-btn:hover {
  transform: translateY(-3px);
  /* leve "subida" do botão */
  box-shadow: 0px 8px 25px rgba(92, 92, 92, 0.3);
  /* sombra maior no hover */
  opacity: 0.90
}

</style>
