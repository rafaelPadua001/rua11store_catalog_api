<template>
    <v-container>
        <div v-if="isLoading">Carregando...</div>

        <div v-else-if="post">
            <v-card elevation="0">
                <v-card-text>
                    <v-row>
                        <v-col cols="3">
                            <v-card elevation="1">
                                <v-card-title>Últimas Notícias</v-card-title>

                                <v-divider></v-divider>

                                <v-card-text>
                                    <div v-for="post in posts.slice(0, 5)" :key="post.id" class="mb-3">
                                        <v-card outlined elevation="0">
                                            <v-row no-gutters align="center">
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
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-col>

                        <v-col cols="8">
                            <v-card>
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
                                                
                                                <!-- Conteúdo do Post -->
                                                <div v-html="post.content"></div>
                                            </v-card>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                            </v-card>

                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>

        </div>

        <div v-else>
            <p>Nenhum post encontrado.</p>
        </div>
    </v-container>
</template>

<script>
import axios from "axios";

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
            psots: [],
            isLoading: false,
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
                }
            } catch (error) {
                console.error("Erro ao carregar post:", error);
            } finally {
                this.isLoading = false;
            }
        },
    },
};
</script>
