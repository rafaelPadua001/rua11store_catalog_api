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
                                        <p class="mb-2 text-h4">{{ post.title }}</p>
                                        <v-divider></v-divider>

                                        <p class="text-caption mb-2" align="end">{{ formatDate(post.created_at) }}</p>

                                        <!-- Imagem Cover -->
                                        <v-img :src="post.cover_image" height="300px" class="srounded" />
                                        <v-row>
                                            <v-col cols="12" md="12" sm="4">
                                                <v-card elevation="0" class="pa-0">
                                                    <v-card-text>
                                                        <div class="d-flex flex-wrap justify-center align-center">
                                                            <span class="mr-0 font-weight-medium">Compartilhar:</span>

                                                            <!-- Facebook -->
                                                            <!-- No seu componente Vue, atualize o botão do Facebook -->
                                                            <v-btn icon variant="text" color="blue"
                                                                :href="`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent('https://rua11store-catalog-api-lbp7.onrender.com/blog/share/' + post.slug + '?v=' + new Date().getTime())}`"
                                                                target="_blank">
                                                                <v-icon>mdi-facebook</v-icon>
                                                            </v-btn>

                                                            <!-- <v-btn icon variant="text" color="purple"
                                                                @click="shareOnInstagram(post)"
                                                                target="_blank">
                                                                <v-icon>mdi-instagram</v-icon>
                                                            </v-btn> -->
                                                            <!-- WhatsApp -->
                                                            <v-btn icon variant="text" color="green"
                                                                :href="`https://api.whatsapp.com/send?text=${encodeURIComponent('https://rua11store-catalog-api-lbp7.onrender.com/blog/share/' + post.slug + '?v=' + new Date().getTime())}`"
                                                                target="_blank">
                                                                <v-icon>mdi-whatsapp</v-icon>
                                                            </v-btn>

                                                            <!-- Twitter -->
                                                            <v-btn icon variant="text" color="blue-darken-2"
                                                                :href="`https://twitter.com/intent/tweet?url=${encodeURIComponent(baseUrl + '/blog/share/' + post.slug)}&text=${encodeURIComponent(post.title)}`"
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
                                        <div>
                                            <component v-for="(node, index) in parsedContent" :key="index"
                                                :is="node.type === 'ad-banner' ? 'ad-banner' : 'div'"
                                                v-bind="node.type === 'ad-banner' ? { slot: node.attrs.slot, format: node.attrs.format } : {}"
                                                v-html="node.type === 'text' ? node.content : null" />
                                        </div>

                                        <div>
                                            <v-row>
                                                <v-col cols="12">
                                                    <v-card>
                                                        <v-toolbar color="transparent" density="compact">
                                                            <v-toolbar-title class="text-body-1">
                                                                Comments: ({{ this.comments.length }})
                                                            </v-toolbar-title>
                                                        </v-toolbar>

                                                        <v-divider></v-divider>

                                                        <v-card-text>
                                                            <commentInputForm :postId="post.id"
                                                                @create:comment="setComment" @update:user="setUser" />
                                                        </v-card-text>
                                                        <v-divider></v-divider>
                                                        <v-card-text>
                                                            <v-row
                                                                v-for="comment in comments.filter(c => c.status !== 'removed')"
                                                                :key="comment.id" align="start" class="mb-4" no-gutters>
                                                                <!-- Avatar pequeno à esquerda -->
                                                                <v-col cols="2" sm="1" class="d-flex justify-center">
                                                                    <v-avatar>
                                                                        <v-img
                                                                            :src="comment.user_avatar || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'"
                                                                            class="rounded-circle" contain />
                                                                    </v-avatar>
                                                                </v-col>

                                                                <!-- Conteúdo do comentário à direita -->
                                                                <v-col cols="10" sm="11">
                                                                    <div class="d-flex flex-wrap align-center mb-1">
                                                                        <span class="font-weight-medium text-body-2">
                                                                            {{ comment.username || 'Anônimo' }}
                                                                        </span>

                                                                        <!-- Botões de ação -->
                                                                        <div class="ml-auto d-flex flex-wrap">
                                                                            <!-- Denunciar: só se não for dono do comentário -->
                                                                            <v-btn
                                                                                v-if="user && user.id !== comment.user_id && comment.status !== 'reported'"
                                                                                variant="plain" size="x-small"
                                                                                color="red"
                                                                                @click="reportComment(comment)"
                                                                                title="Denunciar">
                                                                                Denunciar
                                                                            </v-btn>

                                                                            <!-- Remover: só se for dono -->
                                                                            <v-btn
                                                                                v-if="user && user.id === comment.user_id"
                                                                                variant="text" size="x-small"
                                                                                color="primary"
                                                                                @click="removeComment(comment)"
                                                                                title="Remover">
                                                                                Remover
                                                                            </v-btn>
                                                                        </div>
                                                                    </div>

                                                                    <!-- Texto do comentário -->
                                                                    <div v-if="comment.status === 'reported'"
                                                                        class="text-body-2 text-grey">
                                                                        <span class="d-inline-block text-truncate"
                                                                            style="max-width: 100%; overflow: hidden;">
                                                                            {{ comment.text }}
                                                                        </span>
                                                                        <v-chip size="x-small" color="red"
                                                                            variant="outlined" class="ml-2">
                                                                            Reported
                                                                        </v-chip>
                                                                    </div>
                                                                    <div v-else class="text-body-2">
                                                                        {{ comment.text }}

                                                                    </div>

                                                                    <!-- Cabeçalho do comentário -->
                                                                    <div class="d-flex justify-end mb-1">
                                                                        <span class="text-caption grey--text"
                                                                            style="font-size: 0.65rem;">
                                                                            {{ formatDate(comment.created_at) }}
                                                                        </span>
                                                                    </div>
                                                                </v-col>

                                                                <v-col cols="12">
                                                                    <v-divider />
                                                                </v-col>
                                                            </v-row>
                                                        </v-card-text>
                                                    </v-card>
                                                </v-col>
                                            </v-row>
                                        </div>
                                    </v-card>
                                </v-col>
                            </v-row>
                        </v-card-text>
                    </v-card>
                </v-col>

                <v-col cols="12" md="3" sm="12">
                    <v-card elevation="1">
                        <v-card-title>Últimas Notícias</v-card-title>

                        <v-divider></v-divider>

                        <v-card-text>
                            <div v-for="post in posts.slice(0, 5)" :key="post.id" class="mb-3">
                                <router-link class="text-decoration-none" :to="`/blog/blogView/${post.slug}`">
                                    <v-card outlined elevation="0">
                                        <v-row>
                                            <!-- Imagem à esquerda -->
                                            <v-col cols="6">
                                                <v-img :src="post.cover_image" height="75" aspect-ratio="1"
                                                    class="rounded" />
                                            </v-col>

                                            <!-- Conteúdo à direita -->
                                            <v-col cols="6">
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
                    <v-snackbar v-model="showToast" timeout="3000" top right :color="toastColor">
                        {{ toastMessage }}
                    </v-snackbar>
                    <v-dialog v-model="reportDialog" max-width="470">
                        <reportComment :comment="comment" @closeReportDialog="handleReportDialogClose" />

                    </v-dialog>
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
import { onMounted, ref, watch } from "vue";
import { h, render } from "vue";
import commentInputForm from "../../comments/commentsView/commentInputForm.vue";
import reportComment from "../../comments/commentsView/reportComment.vue";
import adBanner from "../../adBanner/adBanner.vue";

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    components: {
        commentInputForm,
        reportComment,
        adBanner
    },
    props: ['content'],
    name: "BlogPostView",
    data() {
        return {
            post: null, // post único
            posts: [],
            comments: [],
            user: null,
            isLoading: false,
            baseUrl: window.location.origin,
            reportDialog: false,
            showToast: false,
            toastMessage: '',
            toastColor: 'green'
        };
    },
    created() {
        this.loadPosts();
        this.loadPost();
    },
    computed: {
        parsedContent() {
            if (!this.post || !this.post.content) return [];

            // Decodifica HTML entities
            const htmlString = this.post.content
                .replace(/&lt;/g, '<')
                .replace(/&gt;/g, '>')
                .replace(/&amp;/g, '&');

            const container = document.createElement('div');
            container.innerHTML = htmlString;

            const nodes = [];
            Array.from(container.childNodes).forEach((node) => {
                if (node.tagName === 'AD-BANNER') {
                    nodes.push({
                        type: 'ad-banner',
                        attrs: {
                            slot: node.getAttribute('slot'),
                            format: node.getAttribute('format'),
                        },
                    });
                } else {
                    nodes.push({
                        type: 'text',
                        content: node.outerHTML || node.textContent,
                    });
                }
            });

            return nodes;
        },
    },
    methods: {
        setUser(userData) {
            this.user = userData;
        },
        setComment(commentData) {
            if (!Array.isArray(this.comments)) {
                this.comments = [];
            }
            this.comments.push(commentData);
        },
        formatDate(date) {
            return new Date(date).toLocaleDateString("pt-BR", {
                day: "2-digit",
                month: "short",
                year: "numeric",
            });
        },
        async reportComment(comment) {
            this.comment = comment;
            this.reportDialog = true;
        },
        handleReportDialogClose(commentId, isError = false) {
            this.reportDialog = false;

            if (commentId) {
                const index = this.comments.findIndex(c => c.id === commentId);
                if (index !== -1) {
                    this.comments[index].status = 'reported';
                }

                this.toastMessage = 'Comentário reportado para a nossa moderação!';
                this.toastColor = 'green';
                this.showToast = true;
            } else if (isError) {
                this.toastMessage = 'Erro ao enviar reporte.';
                this.toastColor = 'red';
                this.showToast = true;
            }
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
        setOpenGraphMetaTags() {
            if (!this.post) {
                console.log('Post não carregado ainda');
                return;
            }

            const title = this.post.title || 'Rua11Store Blog';
            const description = this.post.excerpt || 'Confira este artigo no blog Rua11Store!';
            const image = this.post.cover_image || 'https://res.cloudinary.com/dnfnevy9e/image/upload/v1758308180/cratlzxc3sf2qxelqru8.png';
            const url = window.location.href;

            //console.log('Configurando meta tags:', { title, description, image }); // ✅ DEBUG

            // Meta tags básicas essenciais
            this.updateMetaTag('title', title);
            this.updateMetaTag('description', description);

            // Open Graph obrigatórias
            this.updateMetaTag('og:title', title);
            this.updateMetaTag('og:description', description);
            this.updateMetaTag('og:image', image);
            this.updateMetaTag('og:url', url);
            this.updateMetaTag('og:type', 'article');
            this.updateMetaTag('og:site_name', 'Rua11Store Blog');
            this.updateMetaTag('og:image:width', '1200');
            this.updateMetaTag('og:image:height', '630');

            // Twitter Card
            this.updateMetaTag('twitter:card', 'summary_large_image');
            this.updateMetaTag('twitter:title', title);
            this.updateMetaTag('twitter:description', description);
            this.updateMetaTag('twitter:image', image);

            document.title = title;
        },
        // ✅ MÉTODO AUXILIAR PARA ATUALIZAR/CRIAR META TAGS
        updateMetaTag(property, content) {
            let metaTag = document.querySelector(`meta[property="${property}"]`) ||
                document.querySelector(`meta[name="${property}"]`);

            if (!metaTag) {
                metaTag = document.createElement('meta');
                if (property.startsWith('og:')) {
                    metaTag.setAttribute('property', property);
                } else {
                    metaTag.setAttribute('name', property);
                }
                document.head.appendChild(metaTag);
            }

            metaTag.setAttribute('content', content);
        },
        //shareOnInstagram(post) {
        //    const postUrl = `${this.baseUrl}/blog/blogView/${post.slug}`;
        //
        //    // Regex sem aspas ✅
        //    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        //
        //    if (isMobile) {
        //        const imageUrl = post.cover_image || "https://exemplo.com/imagem-padrao.png";
        //        window.location.href = `instagram://story-camera?source_url=${encodeURIComponent(imageUrl)}`;
        //    } else {
        //        navigator.clipboard.writeText(postUrl).then(() => {
        //            alert("✅ Link copiado! Abra o Instagram e cole na sua bio ou post.");
        //        });
        //    }
        //},
        async loadPost() {
            this.isLoading = true;
            try {
                // pega slug da rota
                const slug = this.$route.params.slug;
                const response = await api.get(`/blog/posts/${slug}`); // rota GET única
                const data = response.data.post;

                if (data) {
                    this.post = data;
                    this.setOpenGraphMetaTags();
                    this.loadSeo(this.post);
                    this.loadPostComments();
                    this.renderAdBanners();
                    this.addPostView(this.post);
                    
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
        },
        async loadPostComments() {
            try {
             //   console.log(this.post);
                const response = await api.get(`/post-comment/post-comment/${this.post.id}`);
                this.comments = response.data;
            } catch (e) {
                console.error("Erro ao carregar post_comments", e);
            }
        },
        async removeComment(comment) {
            try {
               // console.log(comment);
                if (!confirm("Tem certeza que deseja remover este produto permanentemente ?")) return;

                try {
                    const response = await api.delete(`/post-comment/post-comment/${comment.id}`)
                    this.comments = this.comments.filter(c => c.id !== comment.id);
                } catch (e) {
                    return console.log('erro ao remover comentário', e.message);
                }
            }
            catch (e) {
                console.log('Erro ao deletar comentário');
            }
        },
        async reportComment(comment) {
            this.comment = comment;
            this.reportDialog = true;
        },
        renderAdBanners() {
            this.$nextTick(() => {
                const container = this.$el.querySelector("[v-html]");
                if (!container) return;

                const placeholders = container.querySelectorAll("ad-banner");

                placeholders.forEach((el) => {
                    // Pega os atributos definidos no post.content
                    const slot = el.getAttribute("slot");
                    const format = el.getAttribute("format") || "auto";
                    const responsive = el.getAttribute("responsive") || "true";

                    // Renderiza o componente Vue no lugar
                    render(
                        h(AdBanner, {
                            slot,
                            format,
                            responsive
                        }),
                        el
                    );
                });
            });
        },
        async addPostView(post){
            try{
                response = await api.post(`/post-views/${post.id}`)
                const data = response.data;
                console.log(data);
            }
            catch(e){
                console.log('error:', e.message);
            }
        },
        async close() {
            this.reportDialog = false;
        }
    },
    // ✅ ATUALIZA META TAGS QUANDO A ROTA MUDA
    watch: {
        '$route.params.slug': {
            handler() {
                this.loadPost();
            },
            immediate: false
        }
    }
};
</script>
