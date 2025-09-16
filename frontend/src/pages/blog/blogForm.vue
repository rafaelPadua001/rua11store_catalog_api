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

export default {
    props: {
        formTitle: { type: String, default: "Novo Post" },
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
            if (this.form.cover_image_file) {
                formData.append("cover_image", this.form.cover_image_file);
            }

            try {
                const url = this.editedPost.id
                    ? `/blog/${this.editedPost.id}`
                    : `/blog/posts`;
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
        },
    },
};
</script>
