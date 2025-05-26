<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="12" xl="12">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Pages Management</h1>
                </v-card-title>

                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newPageItem" class="mb-2">
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="pages" :items-per-page="10" class="elevation-1" item-key="id"
                    fixed-header height="500" :loading="loading" loading-text="Loading pages...">
                    <!-- Exibe imagens de produtos -->
                    <template v-slot:item.title="{ item }">
                        <span>{{ item.title }}</span>
                    </template>
                    <template v-slot:item.content="{ item }">
                        <span>{{ item.content }}</span>
                    </template>

                    <template v-slot:item.actions="{ item }">
                        <v-btn :to="`/menagementPage/pageView/${item.id}`" color="primary" small>
                            Ver Página
                        </v-btn>
                        <v-icon small color="primary" @click.stop="editPage(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small color="error" @click.stop="deletePage(item.id)">
                            mdi-delete
                        </v-icon>
                    </template>

                </v-data-table>

                <v-dialog v-model="dialogPageItem" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">New Page</span>
                        </v-card-title>
                        <v-divider></v-divider>

                        <v-card-subtitle>
                            <v-container>
                                <v-form @submit.prevent="savePage">
                                    <v-text-field v-model="editedPage.name" label="Name" required />
                                    <v-text-field v-model="editedPage.title" label="Título" required />

                                    <!-- <v-textarea v-model="editedPage.content" label="Conteúdo" required /> -->
                                <!-- TOOLBAR -->
    <div class="mb-2">
      <v-btn small @click="editor.chain().focus().toggleBold().run()" :color="editor.isActive('bold') ? 'primary' : ''">
        Bold
      </v-btn>
      <v-btn small @click="editor.chain().focus().toggleItalic().run()" :color="editor.isActive('italic') ? 'primary' : ''">
        Italic
      </v-btn>
      <v-btn small @click="editor.chain().focus().toggleBulletList().run()" :color="editor.isActive('bulletList') ? 'primary' : ''">
        Lista
      </v-btn>
    </div>

    <!-- EDITOR -->
    <editor-content :editor="editor" class="editor-content" />
                                </v-form>
                            </v-container>
                        </v-card-subtitle>

                        <v-card-actions>
                            <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
                            <v-btn color="primary" text @click="savePage">Save</v-btn>
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
    props: ['id'],
    data() {
        return {
            loading: false,
            editor: null,
            pages: [],
            page: {
                title: "",
                content: "",
            },
            editedIndex: -1,
            editedPage: null,
            headers: [
                { title: "ID", key: "id" },
                // { title: "User ID", key: "user_id" },
                { title: "Name", key: "name" },
                { title: "Title", key: "title" },
                { title: "Content", key: "content", align: "right" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
            ],
            isPaymentButtonPayTagDisabled: true,
            isCheckitemButton: true,
            dialogPageItem: false,
            defaultProduct: {
                id: null,
                name: "",
                title: "",
                description: "",

            },
        };

    },
    watch: {
        editedPage: {
            handler(newVal){
                if(this.editor && newVal?.content !== undefined){
                    this.editor.commands.setContent(newVal.content || '<p></p>');
                }
            }
        },
        deep: true,
    },
    // computed: {
    //    
    // },
    async created() {
        this.loadpages();
        this.editor = new Editor({
            extensions: [StarterKit],
            content: '<p>Escreva aqui...</p>', // Conteúdo inicial
            onUpdate: ({ editor }) => {
                this.editedPage.content = editor.getHTML(); // Atualiza o conteúdo do modelo
            }
        });
        if (this.id) {
            const res = await api.get(`/pages/${this.id}`);
            this.page = await res.json();
        }
    },
    beforeUnmount(){
        if(this.editor){
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
        newPageItem() {
            this.editedPage = { ...this.defaultPage };
            this.dialogPageItem = true;
        },
        editPage(item) {
            this.editedIndex = this.pages.findIndex((page) => page.id === item.id);
            this.editedPage = { ...item };
            this.dialogPageItem = true;
        },
        close() {
            this.dialogPageItem = false;
            this.editedPage = { ...this.defaultProduct }; // Mantém um objeto válido
            this.editedIndex = -1;
        },
        async savePage() {
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
                    response = await api.post('/pages/pages', {
                        name: this.editedPage.name,
                        title: this.editedPage.title,
                        content: this.editedPage.content
                    }, config);
                    this.pages.push(response.data.page);
                    this.loading = false;
                    this.close();
                } else {
                    response = await api.put(`/pages/pages/${this.editedPage.id}`, this.editedPage, config);
                    Object.assign(this.pages[this.editedIndex], response.data.page);
                    this.loading = false;
                    this.close();
                }
                return this.close();
            } catch (error) {
                console.error("Error saving page:", error);
            }
        },
        async deletePage(pageId) {
            if (!confirm("Tem certeza que deseja remover esta página permanentemente ?")) return;

            try {
                const token = localStorage.getItem('user_token')
                if (!token) return this.$router.push('/login')

                await api.delete(`/pages/pages/${pageId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                //Remove product from local list
                this.pages = this.pages.filter(page => page.id !== pageId);

                this.$toast.success('Produto removido com sucesso');
            }
            catch (error) {
                console.log("Error deleting product:", error);
                //this.$toast.error("Erro ao excluir produto");
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