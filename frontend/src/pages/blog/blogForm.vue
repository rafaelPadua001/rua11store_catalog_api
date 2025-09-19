<template>
  <v-card>
    <v-card-title>
      <span class="headline">{{ formTitle }}</span>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="valid" lazy-validation>
        <!-- Título da Página -->
        <v-text-field v-model="form.page_title" label="Página" disabled></v-text-field>

        <!-- Título -->
        <v-text-field
          v-model="form.title"
          label="Título"
          :rules="[v => !!v || 'Título é obrigatório']"
          required
          @input="generateSlug"
        ></v-text-field>

        <!-- Slug (read-only) -->
        <v-text-field v-model="form.slug" label="Slug" readonly></v-text-field>

        <!-- Resumo -->
        <v-textarea v-model="form.excerpt" label="Resumo (opcional)" rows="2"></v-textarea>

        <!-- Conteúdo -->
        <v-textarea
          v-model="form.content"
          label="Conteúdo"
          rows="6"
          :rules="[v => !!v || 'Conteúdo é obrigatório']"
          required
        ></v-textarea>

        <v-divider class="my-4"></v-divider>
        <h3>Configurações de SEO</h3>

        <v-text-field v-model="form.keywords" label="Keywords" outlined dense></v-text-field>
        <v-textarea v-model="form.description" label="Meta Description" outlined rows="2" dense></v-textarea>
        <v-text-field v-model="form.canonical_url" label="Canonical URL" outlined dense></v-text-field>
        <v-text-field v-model="form.og_title" label="Open Graph Title" outlined dense></v-text-field>
        <v-textarea v-model="form.og_description" label="Open Graph Description" outlined rows="2" dense></v-textarea>
        <v-text-field v-model="form.og_image" label="Open Graph Image URL" outlined dense></v-text-field>

        <!-- Imagem de Capa -->
        <v-file-input
          v-model="form.cover_image_file"
          label="Imagem de Capa"
          accept="image/*"
          prepend-icon="mdi-image"
        ></v-file-input>

        <!-- Preview da imagem -->
        <v-img
          v-if="form.cover_image_preview || form.cover_image_backend"
          :src="form.cover_image_preview || resolveImageUrl(form.cover_image_backend)"
          max-height="200"
          class="mt-2"
        ></v-img>
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

const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://rua11store-catalog-api-lbp7.onrender.com";

export default {
  props: {
    formTitle: { type: String, default: "Novo Post" },
    editedIndex: { type: Number },
    editedPost: { type: Object, default: () => ({}) },
    page_id: { type: Number, required: true },
    page_title: { type: String, default: "Blog" },
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
        cover_image_file: null,        // arquivo selecionado
        cover_image_preview: null,     // preview do arquivo selecionado
        cover_image_backend: null,     // URL da imagem do backend
        // SEO
        keywords: "",
        description: "",
        canonical_url: "",
        og_title: "",
        og_description: "",
        og_image: "",
      },
      api: axios.create({
        baseURL: API_BASE,
        headers: { "Content-Type": "application/json" },
      }),
    };
  },
  watch: {
    editedPost: {
      immediate: true,
      handler(post) {
        if (post && Object.keys(post).length > 0) {
          this.loadPostData(post);
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
  mounted() {
    if (this.editedPost && Object.keys(this.editedPost).length > 0) {
      this.loadPostData(this.editedPost);
    }
  },
  methods: {
    loadPostData(post) {
      // Dados do post
      this.form.title = post.title || "";
      this.form.slug = post.slug || "";
      this.form.excerpt = post.excerpt || "";
      this.form.content = post.content || "";
      this.form.cover_image_backend = post.cover_image || null;

      // Dados de SEO
      const seo = post.seo || {};
      this.form.keywords = seo.keywords || "";
      this.form.description = seo.description || "";
      this.form.canonical_url = seo.canonical_url || "";
      this.form.og_title = seo.og_title || "";
      this.form.og_description = seo.og_description || "";
      this.form.og_image = seo.og_image || "";
    },
    generateSlug() {
      if (this.form.title) {
        this.form.slug = this.form.title
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-+|-+$/g, "");
      }
    },
    resolveImageUrl(path) {
      if (!path) return null;
      if (path.startsWith("http")) return path;
      return `${API_BASE}/${path}`;
    },
    async savePost() {
      if (!this.$refs.form.validate()) return;

      const formData = new FormData();

      Object.keys(this.form).forEach(key => {
        if (key !== "cover_image_file" && key !== "cover_image_preview" && key !== "cover_image_backend") {
          formData.append(key, this.form[key]);
        }
      });

      if (this.form.cover_image_file) {
        formData.append("cover_image", this.form.cover_image_file);
      }

      const url = this.editedPost?.id
        ? `/blog/posts/${this.editedPost.id}`
        : `/blog/posts`;
      const method = this.editedPost?.id ? "put" : "post";

      const response = await this.api({
        method,
        url,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      });

      const event = this.editedPost?.id ? "update-post" : "save-post";
      this.$emit(event, response.data.post);
      this.$emit("close");
    },
  },
};
</script>
