<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="12" xl="12">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">SEO Management</h1>
                </v-card-title>

                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newSeoItem" class="mb-2">
                        <v-icon left>mdi-plus</v-icon>
                        Add SEO
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="seo" :items-per-page="10" class="elevation-1" item-key="id"
                    fixed-header height="500" :loading="loading" loading-text="Loading pages...">
                    <!-- Exibe imagens de produtos -->
                    <template v-slot:item.title="{ item }">
                        <span>{{ item.metaTitle }}</span>
                    </template>
                    <template v-slot:item.content="{ item }">
                        <span>{{ item.metaDescription }}</span>
                    </template>

                    <template v-slot:item.actions="{ item }">
                        <v-icon small color="primary" @click.stop="editSeo(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small color="error" @click.stop="deleteSeo(item.id)">
                            mdi-delete
                        </v-icon>
                    </template>

                </v-data-table>

                <v-dialog v-model="dialogSeoItem" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">New Page</span>
                        </v-card-title>
                        <v-divider></v-divider>

                        <v-card-subtitle>
                            <v-container>
                                <v-form @submit.prevent="saveSeo">
                                    <v-select v-model="editedSeo.route" :items="pages" item-text="name"
                                        item-value="id" label="Rota da Página" required :return-object="false" />

                                    <v-text-field v-model="editedSeo.metaTitle" label="Título da Página" required />
                                    <v-textarea v-model="editedSeo.metaDescription" label="Meta Descrição" required />
                                    <v-text-field v-model="editedSeo.metaKeywords"
                                        label="Palavras-chave (separadas por vírgula)" />
                                    <v-text-field v-model="editedSeo.ogTitle" label="OG: Título para Redes Sociais" />
                                    <v-textarea v-model="editedSeo.ogDescription"
                                        label="OG: Descrição para Redes Sociais" />
                                    <v-text-field v-model="editedSeo.ogImage" label="OG: URL da Imagem" />

                                    <!-- TOOLBAR (opcional, pode remover se não usar editor) -->
                                    <!-- <div class="mb-2">
        <v-btn small @click="editor.chain().focus().toggleBold().run()"
          :color="editor.isActive('bold') ? 'primary' : ''">
          Bold
        </v-btn>
        <v-btn small @click="editor.chain().focus().toggleItalic().run()"
          :color="editor.isActive('italic') ? 'primary' : ''">
          Italic
        </v-btn>
        <v-btn small @click="editor.chain().focus().toggleBulletList().run()"
          :color="editor.isActive('bulletList') ? 'primary' : ''">
          Lista
        </v-btn>
      </div> -->

                                    <!-- EDITOR (opcional, pode ser removido se não usar conteúdo HTML) -->
                                    <!-- <editor-content :editor="editor" class="editor-content" /> -->
                                </v-form>
                            </v-container>
                        </v-card-subtitle>


                        <v-card-actions>
                            <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
                            <v-btn color="primary" text @click="saveSeo">Save</v-btn>
                        </v-card-actions>


                    </v-card>
                </v-dialog>
            </v-card>


        </v-col>
    </v-row>
</template>

<script>
import axios from "axios";
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { useHead } from '@vueuse/head';



const api = axios.create({
    baseURL: window.location.hostname === "localhost"
        ? "http://localhost:5000"
        : "https://rua11storecatalogapi-production.up.railway.app",
    headers: { "Content-Type": "application/json" },
});

export default {
    components: {
        EditorContent
    },
    // props: ['id'],
    data() {
        return {
            loading: false,
            editor: null,
            pages: [],
            seo: [],
            page: {
                title: "",
                content: "",
            },
            editedIndex: -1,
            editedSeo: null,
            headers: [
                { title: "ID", key: "id" },
                { title: "PageId", key: "route" },
                { title: "Meta Title", key: "metaTitle" },
                { title: "Meta Description", key: "metaDescription" },
                { title: "Meta Keywords", key: "metaKeywords" },
                { title: "OG Title", key: "ogTitle" },
                { title: "OG Description", key: "ogDescription" },
                { title: "OG Image", key: "ogImage" },
                { title: "Title", key: "title" },
                { title: "Content", key: "content", align: "right" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
            ],
            isPaymentButtonPayTagDisabled: true,
            isCheckitemButton: true,
            dialogSeoItem: false,
            defaultSeo: {
                id: null,
                route: "",
                metaTitle: "",
                metaDescription: "",
                metaKeywords: "",
                ogTitle: "",
                ogDescription: "",
                ogImage: "",
                content: "",
            }

        };

    },
    watch: {
        editedSeo: {
            handler(newVal) {
                if (newVal) {
                    useHead({
                        title: newVal.metaTitle || 'Título padrão',
                        meta: [
                            { name: 'description', content: newVal.metaDescription || 'Descrição padrão' },
                            { name: 'keywords', content: newVal.metaKeywords || '' },
                            { property: 'og:title', content: newVal.ogTitle || '' },
                            { property: 'og:description', content: newVal.ogDescription || '' },
                            { property: 'og:image', content: newVal.ogImage || '' }
                        ]
                    });
                }
            },
            immediate: true,
            deep: true
        }
    },

    // computed: {
    //    
    // },
    async created() {
        this.loadpages();
        this.loadSeo();
        this.editor = new Editor({
            extensions: [StarterKit],
            content: '<p>Escreva aqui...</p>', // Conteúdo inicial
            onUpdate: ({ editor }) => {
                this.editedSeo.content = editor.getHTML(); // Atualiza o conteúdo do modelo
            }
        });
        if (this.id) {
            const res = await api.get(`/pages/${this.id}`);
            this.page = await res.json();
        }

        useHead({
            title: this.editedSeo?.metaTitle || 'Título padrão',
            meta: [
                {
                    name: 'description',
                    content: this.editedSeo?.metaDescription || 'Descrição padrão'
                },
                {
                    name: 'keywords',
                    content: this.editedSeo?.metaKeywords || ''
                },
                {
                    property: 'og:title',
                    content: this.editedSeo?.ogTitle || ''
                },
                {
                    property: 'og:description',
                    content: this.editedSeo?.ogDescription || ''
                },
                {
                    property: 'og:image',
                    content: this.editedSeo?.ogImage || ''
                }
            ]
        });
    },
    beforeUnmount() {
        if (this.editor) {
            this.editor.destroy();
        }
    },
    methods: {
        async loadpages() {
            this.loading = true;
            try {
                const response = await api.get("/pages/pages");
                return this.pages = response.data.pages;
            } catch (error) {
                console.error("Error loading pages:", error);
            } finally {
                this.loading = false;
            }
        },
        async loadSeo() {
            this.loading = true;
            try {
                const response = await api.get("/seo/seo");
                return this.seo = response.data.seo;
            } catch (error) {
                console.error("Error loading pages:", error);
            } finally {
                this.loading = false;
            }
        },
        newSeoItem() {
            this.editedSeo = { ...this.defaultSeo };
            this.dialogSeoItem = true;
        },
        editSeo(item) {
            this.editedIndex = this.seo.findIndex((seo) => seo.id === item.id);
            this.editedSeo = { ...item };
            this.dialogSeoItem = true;
        },
        close() {
            this.dialogSeoItem = false;
            this.editedSeo = { ...this.defaultSeo }; // Mantém um objeto válido
            this.editedIndex = -1;
        },
        async saveSeo() {
            this.loading = true;
            try {
                const token = localStorage.getItem('user_token');

                if (!token) return this.$router.push('/login');

                const config = {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                };
                let response;
                if (this.editedIndex === -1) {
                    response = await api.post('/seo/seo', {
                        route: this.editedSeo.route,
                        metaTitle: this.editedSeo.metaTitle,
                        metaDescription: this.editedSeo.metaDescription,
                        metaKeywords: this.editedSeo.metaKeywords,
                        ogTitle: this.editedSeo.ogTitle,
                        ogDescription: this.editedSeo.ogDescription,
                        ogImage: this.editedSeo.ogImage
                    }, config);
                    this.seo.push(response.data.seo);
                    this.loading = false;
                    this.close();
                } else {
                    response = await api.put(`/seo/seo/${this.editedSeo.id}`, this.editedSeo, config);
                    Object.assign(this.seo[this.editedIndex], response.data.seo);
                    this.loading = false;
                    this.close();
                }
                return this.close();
            } catch (error) {
                console.error("Error saving SEO:", error);
            }
        },
        async deleteSeo(seoId) {
            if (!confirm("Tem certeza que deseja remover este item de SEO permanentemente ?")) return;

            try {
                const token = localStorage.getItem('user_token')
                if (!token) return this.$router.push('/login')

                await api.delete(`/seo/seo/${seoId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                //Remove SEO from local list
                this.seo = this.seo.filter(page => page.id !== seoId);

                // this.$toast.success('SEO removido com sucesso');
            }
            catch (error) {
                console.log("Error deleting SEO:", error);
                //this.$toast.error("Erro ao excluir SEO");
            }
        },

    }

};
</script>


<style scoped>
.editor-content {
    border: 1px solid #ccc;
    padding: 1rem;
    min-height: 200px;
    border-radius: 4px;
}
</style>