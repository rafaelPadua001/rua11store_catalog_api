<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>SEO Management</h5>
                </v-card-title>
                <v-divider></v-divider>
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

                    <template v-slot:item.ogImage="{ item }">
                        <v-img :src="getImageUrl(item.ogImage)" max-height="50" max-width="50" contain class="rounded" v-if="item.ogImage"/>
                        <span v-else class="grey--text text--darken-1">N/A</span>
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
                                    <v-select v-model="editedSeo.route" :items="pages" item-text="name" item-value="id"
                                        label="Rota da Página" required :return-object="false" />

                                    <v-text-field v-model="editedSeo.metaTitle" label="Título da Página" required />
                                    <v-textarea v-model="editedSeo.metaDescription" label="Meta Descrição" required />
                                    <v-text-field v-model="editedSeo.metaKeywords"
                                        label="Palavras-chave (separadas por vírgula)" />
                                    <v-text-field v-model="editedSeo.ogTitle" label="OG: Título para Redes Sociais" />
                                    <v-textarea v-model="editedSeo.ogDescription"
                                        label="OG: Descrição para Redes Sociais" />
                                    <v-file-input v-model="editedSeo.ogImage" label="OG: Imagem" accept="image/*"
                                        prepend-icon="mdi-image" @change="handleOgImage" />

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
        : "https://rua11store-catalog-api-lbp7.onrender.com",
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
                //{ title: "OG Title", key: "ogTitle" },
               // { title: "OG Description", key: "ogDescription" },
                { title: "OG Image", key: "ogImage" },
               // { title: "Title", key: "title" },
                //{ title: "Content", key: "content", align: "right" },
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
                const token = localStorage.getItem('access_token');

                if (!token) return this.$router.push('/login');

                const formData = new FormData();

                formData.append('route', this.editedSeo.route);
                formData.append('metaTitle', this.editedSeo.metaTitle);
                formData.append('metaDescription', this.editedSeo.metaDescription);
                formData.append('metaKeywords', this.editedSeo.metaKeywords);
                formData.append('ogTitle', this.editedSeo.ogTitle);
                formData.append('ogDescription', this.editedSeo.ogDescription);

                // Se for um arquivo (do v-file-input), adicione diretamente
                if (this.editedSeo.ogImage instanceof File) {
                    formData.append('ogImage', this.editedSeo.ogImage);
                } else if (typeof this.editedSeo.ogImage === 'string') {
                    // Se for uma string (URL já existente), envie como campo separado
                    formData.append('ogImageUrl', this.editedSeo.ogImage);
                }

                const config = {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'  // importante para envio de arquivos
                    }
                };

                let response;
                if (this.editedIndex === -1) {
                    response = await api.post('/seo/seo', formData, config);
                    this.seo.push(response.data.seo);
                } else {
                    response = await api.post(`/seo/seoUpdate/${this.editedSeo.id}`, formData, config);
                    Object.assign(this.seo[this.editedIndex], response.data.seo);
                }

                this.loading = false;
                this.close();
            } catch (error) {
                console.error("Error saving SEO:", error);
                this.loading = false;
            }
        },
        getImageUrl(path){
        //const baseUrl = window.location.hostname === "localhost"
        //    ? "http://localhost:5000"
        //    : "https://rua11store-catalog-api-lbp7.onrender.com";
        return `${path}`; 
       },
        async deleteSeo(seoId) {
            if (!confirm("Tem certeza que deseja remover este item de SEO permanentemente ?")) return;

            try {
                const token = localStorage.getItem('access_token')
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