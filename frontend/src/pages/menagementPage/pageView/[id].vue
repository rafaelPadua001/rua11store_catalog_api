<template>
   <v-row justify="center" no-gutters>
      <v-toolbar color="transparent" v-if="page.name && isBlogPage">
            <v-toolbar-title class="text-h5">
              <strong>{{ page.title }}</strong>
            </v-toolbar-title>
          </v-toolbar>
          <v-divider></v-divider>
              <v-col cols="12" md="8" v-if="page.name && isBlogPage">
                <v-card elevation="0">
                  <v-card-text>
                    <v-row>
                      <v-col v-for="(post, index) in posts" :key="index" cols="12" sm="6" md="6">
                        <v-card elevation="0" class="rounded overflow-hidden">
                           <router-link :to="`/blog/blogView/${post.slug}`">
                          <v-img :src="post.cover_image" aspect-ratio="1" class="rounded">
                            <!-- Overlay apenas na parte inferior -->
                            <div class="pa-2 text-white" 
                              style="position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.5);">
                              <div class="text-h6 font-weight-bold">
                                <span>{{ post.title }}</span>  
                              </div>
                             
                              <div class="text-caption">
                                <span>{{ formatDate(post.created_at) }}</span>
                              </div>
                               <div>
                                  <v-icon icon="mdi-comment"></v-icon>
                                  {{ post.comments.length }}

                                  <v-icon icon="mdi-eye"></v-icon>
                                  {{post.views.length}}
                              </div>
                            </div>
                          </v-img>
                          </router-link>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
        </v-col>
        <v-col cols="12" md="3" sm="12">
          <div v-if="page.name && isBlogPage">
               <v-card elevation="1">
                  <v-card-title>Últimas Notícias</v-card-title>

                  <v-divider></v-divider>

                  <v-card-text>
                    <div v-for="post in posts.slice(0, 5)" :key="post.id">
                      <router-link class="text-decoration-none" :to="`/blog/blogView/${post.slug}`">
                        <v-card outlined elevation="0">
                        <v-row>
                          <!-- Imagem à esquerda -->
                          <v-col cols="6">
                            <v-img :src="post.cover_image"  height="75" aspect-ratio="1" class="rounded" />
                          </v-col>

                          <!-- Conteúdo à direita -->
                          <v-col cols="6">
                            <div class="font-weight-bold">{{ post.title }}</div>
                            <div class="text--secondary">{{ post.excerpt }}</div>
                            <div class="text-caption text--secondary">{{ formatDate(post.created_at) }}</div>
                          </v-col>
                        </v-row>
                      </v-card>
                      </router-link>
                    </div>
                  </v-card-text>
                </v-card>
      </div>
      <div v-else-if="page.name">
        other pages
      </div>
      <div v-else>
        Carregando...
      </div>
        </v-col>
      </v-row>
  <!-- <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto">
       <div class="text-center">
        <v-row justify="center" class="mt-0 mb-4" no-gutters>
          <v-col cols="12">
            <v-divider></v-divider>
            <v-card
              elevation="4"
              :color="page.hero_background_color"
              width="100%"
              class="rounded-lg overflow-hidden hero-card"
              v-if="page.hero_background_color || page.hero_image"
            >
              <v-img
                :src="page.hero_image"
                :alt="page.title"
                max-height="320"
                height="100%"
                class="mx-auto d-block"
              />
              <v-card-text v-if="page.hero_title || page.hero_subtitle">
                <v-row justify="center" no-gutters>
                  <v-col cols="auto">{{ page.hero_title }}</v-col>
                </v-row>
                <v-row justify="center">
                  <v-col cols="auto">{{ page.hero_subtitle }}</v-col>
                </v-row>
              </v-card-text>

              <v-card-text v-if="page.hero_buttons && page.hero_buttons.length">
                <v-row justify="center" no-gutters>
                  <v-col v-for="(button, index) in page.hero_buttons" :key="index">
                    <v-btn
                      class="mx-0 text-caption hover-btn"
                      size="x-large"
                      target="_blank"
                      block
                      :color="button.heroButtonBackgroundColor"
                      :href="button.url"
                      variant="elevated"
                      v-if="button.icon && button.icon.value"
                    >
                      <v-icon
                        
                        :icon="button.icon.value"
                        class="mr-1"
                        size="large"
                      ></v-icon>
                      {{ button.label }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Carousel 
        <div
          class="mt-0 mb-1 d-flex justify-center flex-wrap"
          v-if="page.carousel_image && page.carousel_image.length"
        >
          <v-row justify="center" class="my-2">
            <v-col cols="12" sm="10" md="8" lg="6">
              <v-carousel
                :show-arrows="false"
                cycle
                hide-delimiters
                height="350"
                interval="5000"
                v-model="activeIndex"
              >
                <v-carousel-item v-for="(img, index) in page.carousel_image" :key="index">
                  <v-card elevation="0">
                    <v-img :src="img" width="300" height="300" contain class="mx-auto" />
                  </v-card>
                </v-carousel-item>
              </v-carousel>
            </v-col>
          </v-row>
        </div>

        <!-- Content 
        <v-card v-if="page.content">
          <v-card-text>
            <v-card-title class="text-left">{{ page.name }}</v-card-title>
            <v-divider></v-divider>
            <div class="text-body-2 text-left font-weight-light mb-n1" v-html="page.content"></div>
          </v-card-text>
        </v-card>
      </div>
     
      

    </v-responsive>
  </v-container> -->
</template>

<script>
import axios from "axios";
import { useSeo } from "../../../useSeo";

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
      isBlogPage: false,
      page: {
        carousel_image: [],
        hero_image: "",
        hero_title: "",
        hero_subtitle: "",
        title: "",
        content: "",
        hero_buttons: [],

      },
      activeIndex: 0,
      loading: false,
      pages: [],
      posts: [],
    };
  },
  async created() {
    await this.loadPage();
    await this.loadPosts();
  },
  watch: {
    "$route.params.id": {
      immediate: false,
      handler: async function (newId, oldId) {
        if (newId !== oldId) {
          await this.loadPage();
          await this.loadPosts();
        }
      },
    },
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "short",
        year: "numeric"
      });
    },
    async loadPage() {
      this.loading = true;
      try {
        const response = await api.get("/pages/pages"); // usa o api com baseURL
        const pagesData = response.data?.pages || [];
        const currentPageId = this.$route.params.id;

        const foundPage = pagesData.find((p) => p.id == currentPageId);

        if (foundPage) {
          const normalizedPage = {
            ...foundPage,
            name: foundPage.name || "",
            hero_image: foundPage.heroImage || "",
            hero_title: foundPage.heroTitle || "",
            hero_subtitle: foundPage.heroSubtitle || "",
            carousel_image: Array.isArray(foundPage.carouselImages)
              ? foundPage.carouselImages
              : [],
            hero_buttons: Array.isArray(foundPage.heroButtons)
              ? foundPage.heroButtons
              : [],
          };

          this.page = normalizedPage;
          this.isBlogPage = normalizedPage.name.toLowerCase() === "blog";
        }
        else {
          console.warn(`Página ${currentPageId} não encontrada`);
          this.isBlogPage = false;
        }
      } catch (error) {
        console.error("Erro ao carregar páginas:", error);
        this.isBlogPage = false;
      } finally {
        this.loading = false;
      }
    },
    stripHtml(html) {
      const div = document.createElement("div");
      div.innerHTML = html;
      return div.textContent || div.innerText || "";
    },
    async loadSeoFromAPI(pageId) {
      try {
        const { setSeo } = useSeo();
        const response = await axios.get(`/seo/seo/${pageId}`);
        const seoData = response.data?.seo;
        setSeo(seoData || { title: this.page.title || 'Título padrão', description: '', image: '' });
      } catch (err) {
        console.warn(`Página ${pageId} não possui SEO cadastrado`);
        const { setSeo } = useSeo();
        setSeo({ title: this.page.title || 'Título padrão', description: '', image: '' });
      }
    },
    async loadPosts() {
      try {
        const response = await api.get(`/blog/posts`);
        this.posts = response.data;
      }
      catch (e) {
        console.log(e.error);
      }
    }
  },
};
</script>

<style scoped>
.hero-card {
  background-image: radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    repeating-radial-gradient(circle at center, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.05) 10px, transparent 10px, transparent 20px),
    repeating-conic-gradient(rgba(255, 255, 255, 0.05) 0deg 5deg, transparent 5deg 10deg);
  background-size: cover;
  color: white;
  min-height: 375px;
}

.v-btn {
  margin-left: 1px !important;
  margin-right: 1px !important;
}

.hover-btn {
  transition: transform 0.2s, box-shadow 0.2s;
}

.hover-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0px 8px 25px rgba(92, 92, 92, 0.3);
  opacity: 0.9;
}
</style>
