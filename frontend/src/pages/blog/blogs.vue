<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>Blog Management</h5>
                </v-card-title>

                <v-divider></v-divider>

                <v-card-actions class="d-flex justify-end mb-0">
                    <v-btn color="primary" @click="newPost">
                        <v-icon left>mdi-plus</v-icon>
                        Add Post
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="posts" :items-per-page="20" class="elevation-1" item-key="id"
                    fixed-header height="500" :loading="loading" loading-text="Loading posts...">
                    <template v-slot:item.cover_image="{ item }">
                        <v-img :src="item.cover_image" max-width="100" max-height="60"></v-img>
                    </template>
                    <!-- 🔹 Slot para exibir imagens 
                 <template v-slot:item.thumbnail_path="{ item }">
                        <v-img v-if="item.thumbnail_path || (item.image_paths && item.image_paths.length > 0)"
                            :src="getProductImage(item.thumbnail_path || item.image_paths[0], item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="60" min-height="30"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

<!--<template v-slot:item.description="{ item }">
                        <span v-if="item.description && item.description.length > 100">
                            {{ item.description.substring(0, 38) }}...
                        </span>
                        <span v-else>
                            {{ item.description }}
                        </span>
                    </template> -->

                    <!-- 🔹 Slot para categoria
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>

                    <!-- slot para price 
                     <template v-slot:item.price="{item}">
                        <span v-if="item && item.price">R$ {{ item.price }}</span>
                     </template> -->

                    <!-- 🔹 Slot para ações -->
                    <template v-slot:item.actions="{ item }">
                       <!-- <router-link :to="`/products/productView/${item.seo.slug}`">
                            <v-icon small color="primary">mdi-eye</v-icon>
                        </router-link>-->

                        <v-icon small color="primary" @click.stop="editProduct(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small color="error" @click.stop="deleteProduct(item.id)">
                            mdi-delete
                        </v-icon>
                    </template> 
                </v-data-table>

            </v-card>

            <!-- Modal para Adicionar/Editar Produto -->
            <v-dialog v-model="newPostDialog" max-width="600" fullscreen>
                <BlogForm :page_id="this.form.page_id" :page_title="formTitle" :form-title="formTitle" @close="close"
                    @save-post="addPost" />

            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
import axios from "axios";
import BlogForm from "./blogForm.vue";
//   import { directive as mask } from "v-mask";


const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    components: {
        BlogForm,
    },
    data() {
        return {
            loading: false,
            newPostDialog: false,
            pages: [],
            posts: [],
            form: {
                page_id: null,  // será preenchido com o id da página Blog
                title: "",
                slug: "",
                excerpt: "",
                content: "",
                cover_image_file: null,
                cover_image_preview: null,
            },
            headers: [
                { title: "ID", key: "id", align: "start" },
                { title: "Título", key: "title" },
                { title: "Slug", key: "slug" },
                { title: "Resumo", key: "excerpt" },
                { title: "Imagem de Capa", key: "cover_image", sortable: false },
                { title: "Criado em", key: "created_at" },
                { title: "Atualizado em", key: "updated_at" },
                { title: "Ações", key: "actions", sortable: false },
            ],
        };
    },
    computed: {


    },
    created() {
        this.loadPages();
        this.loadPosts();
    },
    methods: {
        async loadPages() {
            this.loading = true;
            try {
                const response = await api.get('/pages/pages/Blog');
                this.pages.push(response.data);
                this.form.page_id = response.data.id;
            }
            catch (e) {
                console.log(e.error);
            }
            finally {
                this.loading = false;
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
        newPost() {
            // this.editedProduct = { ...this.defaultProduct, seo: { ...this.defaultProduct.seo } };
            this.newPostDialog = true;
        },
        addPost(post) {
            this.posts.push(post);
        },
        close() {
            this.newPostDialog = false;
            // this.editedProduct = { ...this.defaultProduct }; // Mantém um objeto válido
            // this.editedIndex = -1;
        },

    },
};
</script>