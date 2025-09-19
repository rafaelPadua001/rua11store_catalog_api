<template>
    <v-card>
        <v-card-title>
            <span class="headline">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>

                <v-text-field :label="form.page_title" :value="form.page_title" disabled></v-text-field>


                <!-- Título -->
                <v-text-field v-model="form.title" label="Título" :rules="[v => !!v || 'Título é obrigatório']" required
                    @input="generateSlug"></v-text-field>

                <!-- Slug (read-only) -->
                <v-text-field v-model="form.slug" label="Slug" readonly></v-text-field>

                <!-- Resumo -->
                <v-textarea v-model="form.excerpt" label="Resumo (opcional)" rows="2"></v-textarea>

                <!-- Conteúdo -->
                <v-textarea v-model="form.content" label="Conteúdo" rows="6"
                    :rules="[v => !!v || 'Conteúdo é obrigatório']" required></v-textarea>

                <v-divider class="my-4"></v-divider>
                <h3>Configurações de SEO</h3>

                <v-text-field v-model="form.keywords" label="Keywords (separadas por vírgula)" outlined
                    dense></v-text-field>

                <v-textarea v-model="form.description" label="Meta Description" outlined rows="2" dense></v-textarea>

                <v-text-field v-model="form.canonical_url" label="Canonical URL" outlined dense></v-text-field>

                <v-text-field v-model="form.og_title" label="Open Graph Title" outlined dense></v-text-field>

                <v-textarea v-model="form.og_description" label="Open Graph Description" outlined rows="2"
                    dense></v-textarea>

                <v-text-field v-model="form.og_image" label="Open Graph Image URL" outlined dense></v-text-field>

                <!-- Imagem de Capa -->
                <v-file-input v-model="form.cover_image_file" label="Imagem de Capa" accept="image/*"
                    prepend-icon="mdi-image"></v-file-input>

                <!-- Preview da imagem -->
                <v-img v-if="form.cover_image_preview" :src="form.cover_image_preview" max-height="200"
                    class="mt-2"></v-img>


            </v-form>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="$emit('close')">Cancelar</v-btn>
            <v-btn color="primary" @click="savePost" :disabled="!valid">Salvar</v-btn>
        </v-card-actions>
    </v-card>
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
    props: {
        formTitle: { type: String, default: "Novo Post" },
        editedIndex: { type: Number },
        editedPost: { type: Object, default: () => ({}) },
        page_id: { type: Number, required: true },
        page_title: { type: String, default: 'Blog' }
    },
    data() {
        return {
            valid: false,
            form: {
                page_id: this.page_id,
                page_title: this.page_title,
                title: "",
                slug: "",
                excerpt: "",
                content: "",
                cover_image_file: null,
                cover_image_preview: null,

                // SEO
                keywords: "",
                description: "",
                canonical_url: "",
                og_title: "",
                og_description: "",
                og_image: "",
            },
            api: axios.create({
                baseURL:
                    window.location.hostname === "localhost"
                        ? "http://localhost:5000"
                        : "https://rua11store-catalog-api-lbp7.onrender.com",
                headers: { "Content-Type": "application/json" },
            }),
        };
    },
    watch: {
        editedPost: {
            immediate: true,
            handler(post) {
                if (post && Object.keys(post).length > 0) {
                    this.form.title = post.title || "";
                    this.form.slug = post.slug || "";
                    this.form.excerpt = post.excerpt || "";
                    this.form.content = post.content || "";
                    this.form.cover_image_preview = post.cover_image || null;
                    this.form.keywords = post.seo_metadata?.keywords || "";
                    this.form.description = post.seo_metadata?.description || "";
                    this.form.canonical_url = post.seo_metadata?.canonical_url || "";
                    this.form.og_title = post.seo_metadata?.og_title || "";
                    this.form.og_description = post.seo_metadata?.og_description || "";
                    this.form.og_image = post.seo_metadata?.og_image || "";

                }
            },
        },
        "form.cover_image_file"(file) {
            if (file) {
                const reader = new FileReader();
                reader.onload = e => (this.form.cover_image_preview = e.target.result);
                reader.readAsDataURL(file);
            } else {
                this.form.cover_image_preview = null;
            }
        },
    },
    methods: {
        generateSlug() {
            if (this.form.title) {
                this.form.slug = this.form.title
                    .toLowerCase()
                    .replace(/[^a-z0-9]+/g, "-")
                    .replace(/^-+|-+$/g, "");
            }
        },
        async savePost() {
            if (!this.$refs.form.validate()) return;

            const formData = new FormData();
            formData.append("page_id", this.page_id);
            formData.append("title", this.form.title);
            formData.append("slug", this.form.slug);
            formData.append("excerpt", this.form.excerpt);
            formData.append("content", this.form.content);
            formData.append("keywords", this.form.keywords);
            formData.append("description", this.form.description);
            formData.append("canonical_url", this.form.canonical_url);
            formData.append("og_title", this.form.og_title);
            formData.append("og_description", this.form.og_description);
            formData.append("og_image", this.form.og_image);

            if (this.form.cover_image_file) {
                formData.append("cover_image", this.form.cover_image_file);
            }

            if (this.editedIndex === -1) {
                try {
                    const url = `/blog/posts`;
                    const method = this.editedPost.id ? "put" : "post";

                    const response = await this.api({
                        method,
                        url,
                        data: formData,
                        headers: { "Content-Type": "multipart/form-data" },
                    });

                    const savedPost = response.data.post;
                    this.$emit("save-post", savedPost); // alerta o componente pai
                    this.$emit("close");
                } catch (error) {
                    console.error("Erro ao salvar post:", error);
                }
            }
            else {
                const response = await api.put(`/blog/posts/${this.editedPost.id}`, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
                const updatedPost = response.data.post;

                this.$emit("update-post", updatedPost); // alerta o componente pai
                this.$emit("close");

            }
        },
    },
};
</script>
