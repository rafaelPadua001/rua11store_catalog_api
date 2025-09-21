<template>
    <v-container>
        <div v-if="isLoading">Carregando...</div>

        <div v-else-if="post">
            <v-row justify="center">
                <v-col cols="12" md="8">
                    <v-card elevation="0">
                        <v-card-text>
                            <v-row no-gutters justify="center">
                                <v-col cols="12" sm="6" md="12">
                                    <v-card elevation="0" class="rounded overflow-hidden">
                                        <!-- Título -->
                                        <p class="mb-2 text-h3">{{ post.title }}</p>
                                        <v-divider></v-divider>

                                        <p class="text-caption mb-4" align="end">{{ formatDate(post.created_at) }}</p>

                                        <!-- Imagem Cover -->
                                        <v-img :src="post.cover_image" height="300px" class="mb-6 rounded" />
                                        <v-row>
                                            <v-col cols="12">
                                                <v-card elevation="0" class="pa-2">
                                                    <v-card-text>
                                                        <div class="d-flex flex-wrap justify-center align-center">
                                                            <span class="mr-3 font-weight-medium">Compartilhar:</span>

                                                            <!-- WhatsApp -->
                                                            <v-btn icon variant="text" color="green"
                                                                :href="`https://api.whatsapp.com/send?text=${encodeURIComponent(post.title)} - ${baseUrl}/blog/blogView/${post.slug}`"
                                                                target="_blank">
                                                                <v-icon>mdi-whatsapp</v-icon>
                                                            </v-btn>

                                                            <!-- Facebook -->
                                                            <v-btn icon variant="text" color="blue"
                                                                :href="`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(baseUrl + '/blog/blogView/' + post.slug)}`"
                                                                target="_blank">
                                                                <v-icon>mdi-facebook</v-icon>
                                                            </v-btn>

                                                            <!-- X (Twitter) -->
                                                            <v-btn icon variant="text" color="black"
                                                                :href="`https://twitter.com/intent/tweet?url=${encodeURIComponent(baseUrl + '/blog/blogView/' + post.slug)}&text=${encodeURIComponent(post.title)}`"
                                                                target="_blank">
                                                                <v-icon>mdi-twitter</v-icon>
                                                            </v-btn>

                                                            <!-- LinkedIn -->
                                                            <v-btn icon variant="text" color="indigo"
                                                                :href="`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(baseUrl + '/blog/blogView/' + post.slug)}`"
                                                                target="_blank">
                                                                <v-icon>mdi-linkedin</v-icon>
                                                            </v-btn>

                                                            <!-- Email -->
                                                            <v-btn icon variant="text" color="red"
                                                                :href="`mailto:?subject=${encodeURIComponent(post.title)}&body=${encodeURIComponent(baseUrl + '/blog/blogView/' + post.slug)}`"
                                                                target="_blank">
                                                                <v-icon>mdi-email</v-icon>
                                                            </v-btn>
                                                        </div>
                                                    </v-card-text>
                                                </v-card>
                                            </v-col>
                                        </v-row>

                                        <v-divider></v-divider>
                                        <!-- Conteúdo do Post -->
                                        <div v-html="post.content"></div>
                                    </v-card>
                                </v-col>
                            </v-row>


                        </v-card-text>
                    </v-card>
                </v-col>

                <v-col cols="12" md="4" sm="12">
                    <v-card elevation="1">
                        <v-card-title>Últimas Notícias</v-card-title>

                        <v-divider></v-divider>

                        <v-card-text>
                            <div v-for="post in posts.slice(0, 5)" :key="post.id" class="mb-3">
                                <router-link class="text-decoration-none" :to="`/blog/blogView/${post.slug}`">
                                    <v-card outlined elevation="0">
                                        <v-row>
                                            <!-- Imagem à esquerda -->
                                            <v-col cols="4">
                                                <v-img :src="post.cover_image" aspect-ratio="1" class="rounded" />
                                            </v-col>

                                            <!-- Conteúdo à direita -->
                                            <v-col cols="8">
                                                <div class="font-weight-bold">{{ post.title }}</div>
                                                <div class="text--secondary">{{ post.excerpt }}</div>
                                                <div class="text-caption text--secondary">{{
                                                    formatDate(post.created_at) }}</div>
                                            </v-col>
                                        </v-row>
                                    </v-card>
                                </router-link>
                            </div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>

        </div>

        <div v-else>
            <p>Nenhum post encontrado.</p>
        </div>
    </v-container>
</template>

<script>
import axios from "axios";
import { useSeo } from '../../../useSeo';

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    name: "BlogPostView",
    data() {
        return {
            post: null, // post único
            posts: [],
            isLoading: false,
            baseUrl: window.location.origin,
        };
    },
    created() {
        this.loadPosts();
        this.loadPost();
    },
    methods: {
        formatDate(date) {
            return new Date(date).toLocaleDateString("pt-BR", {
                day: "2-digit",
                month: "short",
                year: "numeric",
            });
        },
        async loadPosts() {
            this.loading = true;
            try {
                const response = await api.get('/blog/posts');
                this.posts = response.data;

                // this.form.page_id = response.data.id;
            }
            catch (e) {
                console.log(e.error);
            }
            finally {
                this.loading = false;
            }
        },
        async loadPost() {
            this.isLoading = true;
            try {
                // pega slug da rota
                const slug = this.$route.params.slug;
                const response = await api.get(`/blog/posts/${slug}`); // rota GET única
                const data = response.data.post;

                if (data) {
                    this.post = data;
                    this.loadSeo(this.post);
                }
            } catch (error) {

                console.error("Erro ao carregar post:", error);
            } finally {
                this.isLoading = false;
            }
        },
        async loadSeo() {
            try {
                const { setSeo } = useSeo();
                const response = await api.get(`/post-seo/post_seo/${this.post.id}`);
                const seoData = response.data;

                setSeo({
                    post: this.post,
                    seo: seoData
                });
            } catch (error) {
                const { setSeo } = useSeo();
                console.error("Erro ao carregar post_seo", error);
            }
        }
    },
};
</script>
