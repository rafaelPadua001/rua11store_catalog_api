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
        <v-text-field v-model="form.title" label="Título" :rules="[v => !!v || 'Título é obrigatório']" required
          @input="generateSlug"></v-text-field>

        <!-- Slug -->
        <v-text-field v-model="form.slug" label="Slug" readonly></v-text-field>

        <!-- Resumo -->
        <label class="text-subtitle-2 font-weight-medium mb-1">Resumo (opcional)</label>

        <EditorContent v-if="excerptEditor" :editor="excerptEditor" class="excerpt-editor" />

        <!-- PREVIEW DO HTML -->
        <div v-if="form.excerpt" class="excerpt-preview mt-3 pa-3" v-html="form.excerpt"></div>
        <div>
          <!-- Toolbar do editor -->
          <div v-if="editor" class="editor-toolbar mb-2">
            <v-btn-toggle v-model="toggle" border divided>
              <v-btn @click="addAdBanner" prepend-icon="mdi-plus">
                Inserir Ad Banner
              </v-btn>
              <v-btn @click="toggleBold" :class="{ 'font-bold': isBoldActive }">
                <v-icon icon="mdi-format-bold"></v-icon>
              </v-btn>
              <v-btn @click="toggleItalic" :class="{ 'italic': isItalicActive }">
                <v-icon icon="mdi-format-italic"></v-icon>
              </v-btn>
            </v-btn-toggle>

            <v-btn-toggle v-model="alignment" variant="outlined" divided>
              <v-btn small @click="() => editor.chain().focus().setTextAlign('left').run()">
                <v-icon>mdi-format-align-left</v-icon>
              </v-btn>

              <v-btn small @click="() => editor.chain().focus().setTextAlign('center').run()">
                <v-icon>mdi-format-align-center</v-icon>
              </v-btn>

              <v-btn small @click="() => editor.chain().focus().setTextAlign('right').run()">
                <v-icon>mdi-format-align-right</v-icon>
              </v-btn>

              <v-btn small @click="() => editor.chain().focus().setTextAlign('justify').run()">
                <v-icon>mdi-format-align-justify</v-icon>
              </v-btn>


              <v-btn small @click="insertLink">
                <v-icon left>mdi-link</v-icon>
              </v-btn>
              <v-btn small @click="editor.chain().focus().unsetLink().run()">
                <v-icon left>mdi-link-off</v-icon>

              </v-btn>

            </v-btn-toggle>

          </div>

          <!-- Editor -->
          <EditorContent v-if="editor" :editor="editor" class="editor-content" />
        </div>

        <v-divider class="my-4"></v-divider>
        <h3>Configurações de SEO</h3>

        <v-text-field v-model="form.keywords" label="Keywords" outlined dense></v-text-field>
        <v-textarea v-model="form.description" label="Meta Description" outlined rows="2" dense></v-textarea>
        <v-text-field v-model="form.canonical_url" label="Canonical URL" outlined dense></v-text-field>
        <v-text-field v-model="form.og_title" label="Open Graph Title" outlined dense></v-text-field>
        <v-textarea v-model="form.og_description" label="Open Graph Description" outlined rows="2" dense></v-textarea>
        <v-text-field v-model="form.og_image" label="Open Graph Image URL" outlined dense></v-text-field>

        <!-- Imagem de Capa -->
        <v-file-input v-model="form.cover_image_file" label="Imagem de Capa" accept="image/*"
          prepend-icon="mdi-image"></v-file-input>

        <!-- Preview -->
        <v-img v-if="form.cover_image_preview || form.cover_image_backend"
          :src="form.cover_image_preview || resolveImageUrl(form.cover_image_backend)" max-height="200"
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
import { EditorContent, Editor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import TextAlign from '@tiptap/extension-text-align'
import Link from '@tiptap/extension-link'
import axios from 'axios'

const API_BASE =
  window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://rua11store-catalog-api-lbp7.onrender.com'

export default {
  components: { EditorContent },
  props: {
    formTitle: { type: String, default: 'Novo Post' },
    editedPost: { type: Object, default: () => ({}) },
    page_id: { type: Number, required: true },
    page_title: { type: String, default: 'Blog' },
  },
  data() {
    return {
      valid: false,
      editor: null,
      toggle: null,
      form: {
        page_id: this.page_id,
        page_title: this.page_title,
        title: '',
        slug: '',
        excerpt: '',
        content: '',
        cover_image_file: null,
        cover_image_preview: null,
        cover_image_backend: null,
        keywords: '',
        description: '',
        canonical_url: '',
        og_title: '',
        og_description: '',
        og_image: '',
      },
      isBoldActive: false,
      isItalicActive: false,
      api: axios.create({ baseURL: API_BASE, headers: { 'Content-Type': 'application/json' } }),
    }
  },
  watch: {
    editedPost: {
      immediate: true,
      handler(post) {
        if (post && Object.keys(post).length) this.loadPostData(post)
      },
    },
    'form.cover_image_file'(file) {
      if (file) {
        const reader = new FileReader()
        reader.onload = e => (this.form.cover_image_preview = e.target.result)
        reader.readAsDataURL(file)
      } else {
        this.form.cover_image_preview = null
      }
    },
  },
  computed: {
    isBoldActive() {
      return this.editor && this.editor.isActive('bold')
    },
    isItalicActive() {
      return this.editor && this.editor.isActive('italic')
    },
  },
  mounted() {
    this.editor = new Editor({
      extensions: [StarterKit,
        TextAlign.configure({
          type: ['heading', 'paragraph'],
        }),
        Link.configure({
          openOnClic: false,
          autolink: true,
          linkOnPaste: true,
          validate: href => {
            return href.startsWith('/') || href.startsWith('http') || href.startsWith('https');
          },
        }),
      ],
      content: '<p></p>',
    });
    this.excerptEditor = new Editor({
      extensions: [
        StarterKit,
        TextAlign.configure({ types: ['paragraph'] }),
      ],
      content: this.form.excerpt || '',
      onUpdate: () => {
        this.form.excerpt = this.excerptEditor.getHTML()
      }
    });
  },
  beforeDestroy() {
    if (this.editor) this.editor.destroy()
  },

  methods: {
    loadPostData(post) {
      this.form.title = post.title || ''
      this.form.slug = post.slug || ''
      this.form.excerpt = post.excerpt || ''
      this.form.content = post.content || ''
      this.form.cover_image_backend = post.cover_image || null

      const seo = post.seo || {}
      this.form.keywords = seo.keywords || ''
      this.form.description = seo.description || ''
      this.form.canonical_url = seo.canonical_url || ''
      this.form.og_title = seo.og_title || ''
      this.form.og_description = seo.og_description || ''
      this.form.og_image = seo.og_image || ''

      if (this.editor) this.editor.commands.setContent(this.form.content)
    },
    generateSlug() {
      if (this.form.title) {
        this.form.slug = this.form.title
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-+|-+$/g, '')
      }
    },
    resolveImageUrl(path) {
      if (!path) return null
      return path.startsWith('http') ? path : `${API_BASE}/${path}`
    },
    addAdBanner() {
      const slotId = '1234567890';
      if (!slotId) return
      const adHtml = `<ad-banner slot="${slotId}" format="auto"></ad-banner>`
      this.editor.chain().focus().insertContent(adHtml).run()
    },
    toggleBold() {
      this.editor.chain().focus().toggleBold().run()
    },
    toggleItalic() {
      this.editor.chain().focus().toggleItalic().run()
    },
    alignCenter() {
      this.editor.chain().focus().setTextAlign('center').run();

    },
    setAlign(align) {
      this.editor.chain().focus().setTextAlign(align).run()
    },

    insertLink() {
      const previousUrl = this.editor.getAttributes('link').href;
      const url = prompt('Informe a Url interna:', previousUrl || '/products/productView/');

      if (url === null) return

      if (url === '') {
        //remove url link
        this.editor.chain().focus().unsetLink().run();
        return;
      }

      this.editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
    },
    async savePost() {
      if (!this.$refs.form.validate()) return

      // Atualiza o form.content com o conteúdo atual do editor
      if (this.editor) {
        this.form.content = this.editor.getHTML()
      }

      const formData = new FormData()
      Object.keys(this.form).forEach(key => {
        if (!['cover_image_file', 'cover_image_preview', 'cover_image_backend'].includes(key)) {
          formData.append(key, this.form[key])
        }
      })

      if (this.form.cover_image_file) formData.append('cover_image', this.form.cover_image_file)

      const url = this.editedPost?.id ? `/blog/posts/${this.editedPost.id}` : `/blog/posts`
      const method = this.editedPost?.id ? 'put' : 'post'

      const response = await this.api({
        method,
        url,
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      const event = this.editedPost?.id ? 'update-post' : 'save-post'
      this.$emit(event, response.data.post)
      this.$emit('close')
    },

  },
}
</script>

<style scoped>
.editor-content {
  min-height: 200px;
  border: 1px solid #ccc;
  padding: 10px;

}

.editor-content * {
  outline: none !important;
}

.font-bold {
  font-weight: bold;
}

.italic {
  font-style: italic;
}

.excerpt-preview {
  background: #f8f8f8;
  border-radius: 6px;
  border: 1px solid #ddd;
  font-size: 14px;
  line-height: 1.5;
  min-height: 40px;
}

/* Garante que os alinhamentos funcionam */
.excerpt-preview p {
  margin: 0;
}
</style>