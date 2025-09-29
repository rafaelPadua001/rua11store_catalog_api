<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>Pages Management</h5>
                </v-card-title>
                <v-divider></v-divider>

                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newPageItem" class="mb-2">
                        <v-icon left>mdi-plus</v-icon>
                        Add Page
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
                        <router-link :to="`/menagementPage/pageView/${item.id}`" icon small class="ma-0 pa-0">
                            <v-icon size="20" color="primary">mdi-eye</v-icon>
                        </router-link>

                        <v-icon small color="primary" @click.stop="editPage(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small color="error" @click.stop="deletePage(item.id)">
                            mdi-delete
                        </v-icon>
                    </template>

                </v-data-table>

                <v-dialog v-model="dialogPageItem" max-width="800px" fullscreen>
                    <v-card>
                        <v-card-title>
                            <span class="headline">New Page</span>
                        </v-card-title>
                        <v-divider></v-divider>

                        <v-card-subtitle>
                            <v-container>
                                <v-form @submit.prevent="savePage">
                                    <!-- Dados gerais -->
                                    <v-card>
                                        <v-card-title>Dados Gerais:</v-card-title>
                                        <v-card-text>
                                            <v-text-field v-model="editedPage.name" label="Name" required />
                                            <v-text-field v-model="editedPage.title" label="Título" required />
                                        </v-card-text>
                                    </v-card>
                                    

                                    <!-- HERO -->
                                    <v-card class="mb-4" outlined>
                                        <v-card-title>Seção: Hero</v-card-title>
                                        <v-card-text>
                                            <v-text-field v-model="editedPage.heroTitle" label="Título do Hero" />
                                            <v-text-field v-model="editedPage.heroSubtitle" label="Subtítulo do Hero" />
                                            <v-row>
                                                <v-col cols="4">
                                                    <v-color-picker v-model="editedPage.heroBackgroundColor" hide-canvas
                                                        show-swatches mode="hexa" swatches-max-height="150"
                                                        label="Background Hero color">

                                                    </v-color-picker>
                                                </v-col>
                                                <v-col cols="8" class="d-flex align-center justify-center">
                                                    <v-card height="30%" width="100%" elevation="2"
                                                        :style="{ backgroundColor: editedPage.heroBackgroundColor || '#f5f5f5' }">
                                                        <v-card-text class="text-center white-text">
                                                            Preview Color
                                                        </v-card-text>
                                                    </v-card>
                                                </v-col>
                                            </v-row>

                                            <!-- <v-text-field v-model="editedPage.heroImage" label="URL da Imagem" /> -->
                                            <!-- Hero Image -->
                                            <v-card class="mb-4" outlined>
                                                <v-card-title>Hero Image</v-card-title>

                                                <!-- Lista de URLs -->
                                                <v-card-text>
                                                    <v-row justify="center"
                                                        v-if="editedPage.heroImage && editedPage.heroImage.length >= 1">
                                                        <v-col cols="auto">
                                                            <v-img :src="editedPage.heroImage" contain width="250"
                                                                heigth="200"></v-img>
                                                            <div class="text-center">
                                                                <v-icon color="black"
                                                                    @click="removeHeroImage(index)">mdi-delete</v-icon>
                                                            </div>

                                                        </v-col>
                                                    </v-row>
                                                    <div class="mb-2">

                                                    </div>
                                                    <v-btn small color="primary"
                                                        @click="heroImageDialog = true">Adicionar
                                                        Imagem</v-btn>
                                                </v-card-text>

                                                <v-divider></v-divider>


                                            </v-card>

                                            <!-- Hero buttons -->
                                            <v-card class="mb-4" outlined>
                                                <v-card-title>Hero Buttons</v-card-title>
                                                <v-card-text>
                                                    <v-btn small color="primary" @click="addHeroButton">Adicionar
                                                        Botões
                                                    </v-btn>
                                                    <div v-for="(btn, index) in editedPage.heroButtons" :key="index"
                                                        class="mt-3">
                                                        <v-text-field v-model="btn.label" label="Button Text" dense />
                                                        <v-text-field v-model="btn.url" label="Button URL" />
                                                        <v-combobox v-model="btn.icon" :items="heroIcons"
                                                            item-title="title" item-value="value" density="compact"
                                                            label="Selecionar Ícone">
                                                            <!-- Item na lista (precisa v-bind="props"!) -->
                                                            <template #item="{ props, item }">
                                                                <v-list-item v-bind="props">
                                                                    <template #prepend>
                                                                        <v-icon class="mr-2">{{ item.value }}</v-icon>
                                                                    </template>
                                                                    <v-list-item-title>{{ item.value
                                                                    }}</v-list-item-title>
                                                                </v-list-item>
                                                            </template>

                                                            <!-- Como o selecionado aparece no campo -->
                                                            <template #selection="{ item }">
                                                                <div class="d-flex flex-column">
                                                                    <div class="d-flex align-center">
                                                                        <v-icon class="mr-2">{{ item.value }}</v-icon>
                                                                        <span>{{ item.value }}</span>
                                                                    </div>
                                                                </div>
                                                            </template>
                                                        </v-combobox>

                                                        <v-row no-gutters>
                                                            <v-col cols="4">
                                                                <label for="">Select Button Color:</label>
                                                                <v-color-picker v-model="btn.heroButtonBackgroundColor"
                                                                    hide-canvas show-swatches mode="hexa"
                                                                    swatches-max-height="150"
                                                                    label="Background Hero color">

                                                                </v-color-picker>
                                                            </v-col>
                                                            <v-col cols="4" class="d-flex align-center justify-center" >
                                                                <v-card height="30%" width="100%" elevation="2"
                                                                    :style="{ backgroundColor: editedPage.heroButtonBackgroundColor ?? btn.heroButtonBackgroundColor  }" >
                                                                    <v-card-text class="text-center white--text">
                                                                        Preview Color
                                                                    </v-card-text>
                                                                </v-card>
                                                            </v-col>

                                                            <v-col class="d-flex align-start justify-end">
                                                                <v-btn icon="mdi-delete" color="red" variant="tonal"
                                                                    @click="removeHeroButton(index)"></v-btn>
                                                            </v-col>
                                                        </v-row>

                                                    </div>


                                                </v-card-text>
                                            </v-card>

                                            <v-dialog v-model="heroImageDialog" max-width="800">
                                                <v-card>
                                                    <v-card-title>Visualizar Imagens</v-card-title>
                                                    <v-card-text>
                                                        <v-row justify="center">
                                                            <v-col cols="auto" v-for="(heroImg, index) in uploadsImages"
                                                                :key="index">
                                                                <v-card class="py-2" @click="addHeroImage(heroImg.url)"
                                                                    contain width="250" heigth="200">
                                                                    <v-img :src="heroImg.url" :alt="heroImg.name"
                                                                        contain>
                                                                        <v-card-text>
                                                                            {{ heroImg.url }}
                                                                        </v-card-text>
                                                                    </v-img>
                                                                </v-card>
                                                            </v-col>
                                                        </v-row>

                                                    </v-card-text>
                                                    <v-card-actions>
                                                        <v-spacer></v-spacer>
                                                        <v-btn color="primary" text
                                                            @click="carouselDialog = false">Fechar</v-btn>
                                                    </v-card-actions>
                                                </v-card>
                                            </v-dialog>
                                        </v-card-text>
                                    </v-card>

                                    <!-- CARROSSEL DE PRODUTOS -->
                                    <v-card class="mb-4" outlined>
                                        <v-card-title>Carrossel de Produtos</v-card-title>

                                        <!-- Lista de URLs -->
                                        <v-card-text>
                                            <v-row justify="center">
                                                <v-col cols="auto" v-for="(img, index) in editedPage.carouselImages"
                                                    :key="index">
                                                    <v-img :src="img" contain width="250" heigth="200"></v-img>
                                                    <div class="text-center">
                                                        <v-icon color="black"
                                                            @click="removeCarouselImage(index)">mdi-delete</v-icon>
                                                    </div>

                                                </v-col>
                                            </v-row>
                                            <div class="mb-2">

                                            </div>
                                            <v-btn small color="primary" @click="carouselDialog = true">Adicionar
                                                Imagem</v-btn>
                                        </v-card-text>

                                        <v-divider></v-divider>


                                    </v-card>

                                    <!-- Dialog para exibir imagens -->
                                    <v-dialog v-model="carouselDialog" max-width="800">
                                        <v-card>
                                            <v-card-title>Visualizar Imagens</v-card-title>
                                            <v-card-text>
                                                <v-row>
                                                    <v-col v-for="(product, index) in products" :key="index">
                                                        <v-card class="py-2"
                                                            @click="addCarouselImage(product.thumbnail_path)">
                                                            <v-img :src="product.thumbnail_path" :alt="product.name"
                                                                contain>
                                                                <v-card-text>
                                                                    {{ product.name }}
                                                                </v-card-text>
                                                            </v-img>
                                                        </v-card>
                                                    </v-col>
                                                </v-row>
                                                <v-carousel hide-delimiter-background cycle hide-delimiters
                                                    height="250">
                                                    <v-carousel-item v-for="(img, i) in editedPage.carouselImages"
                                                        :key="i">
                                                        <v-img :src="img" contain />
                                                    </v-carousel-item>
                                                </v-carousel>
                                            </v-card-text>
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn color="primary" text
                                                    @click="carouselDialog = false">Fechar</v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>


                                    <v-card outlined>
                                        <v-card-title>Seção Decriçao:</v-card-title>
                                        <v-card-text>
                                            <v-card  max-width="600" elevation="0">
                                                <div class="d-flex justify-space-between pa-4 pb-0">
                                                    <v-btn-toggle v-model="formatting" variant="outlined" divided
                                                        multiple>
                                                        <v-btn small
                                                            @click="editor.chain().focus().toggleBulletList().run()"
                                                            :color="editor.isActive('bulletList') ? 'primary' : ''">
                                                            <v-icon icon="mdi-format-list-bulleted"></v-icon>
                                                           
                                                        </v-btn>
                                                        <v-btn small @click="editor.chain().focus().toggleBold().run()"
                                                            :color="editor.isActive('bold') ? 'primary' : ''">
                                                           <v-icon icon="mdi-format-bold"></v-icon>
                                                           
                                                        </v-btn>
                                                        <v-btn small
                                                            @click="editor.chain().focus().toggleItalic().run()"
                                                            :color="editor.isActive('italic') ? 'primary' : ''"> 
                                                            <v-icon icon="mdi-format-italic"></v-icon>
                                                        </v-btn>
                                                        
                                                    </v-btn-toggle>

                                                    <v-btn-toggle
                                                        v-model="alignment"
                                                        variant="outlined"
                                                        divided
                                                    >
                                                        <v-btn>
                                                            <v-icon icon="mdi-format-align-center"></v-icon>
                                                            </v-btn>

                                                            <v-btn>
                                                            <v-icon icon="mdi-format-align-left"></v-icon>
                                                            </v-btn>

                                                            <v-btn>
                                                            <v-icon icon="mdi-format-align-right"></v-icon>
                                                            </v-btn>

                                                    </v-btn-toggle>

                                                    <v-btn-toggle
                                                        v-model="alignment"
                                                        variant="outlined"
                                                        divided
                                                    >
                                                        <v-btn  variant="tonal" color="primary">
                                                            upload image
                                                        </v-btn>

                                                           

                                                    </v-btn-toggle>
                                                </div>
                                            </v-card>

                                        </v-card-text>
                                        <v-card-text>
                                            <editor-content :editor="editor" class="editor-content" />
                                        </v-card-text>
                                    </v-card>

                                    <!-- FOOTER -->
                                    <!--<v-card outlined>
                                        <v-card-title>Seção: Footer</v-card-title>
                                        <v-card-text>
                                            <v-textarea v-model="editedPage.footerText" label="Texto do Rodapé" />
                                        </v-card-text>
                                    </v-card>-->


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
        : "https://rua11store-catalog-api-lbp7.onrender.com",
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
            products: [],
            uploadsImages: [],
            page: {
                id: "",
                title: "",
                content: "",
                name: "",
                title: "",
                //  description: "",
                heroTitle: "",
                heroSubtitle: "",
                heroBackgroundColor: "",
                heroImage: "",
                heroButtons: [],
                heroIcon: "",
                carouselImages: [],
                footerText: ""
            },
            editedIndex: -1,
            editedPage: null,
            isPaymentButtonPayTagDisabled: true,
            isCheckitemButton: true,
            dialogPageItem: false,
            heroImageDialog: false,
            carouselDialog: false,
            heroIcons: [
                { title: 'Android', value: 'mdi-android' },
                { title: 'Apple', value: 'mdi-apple' },
                { title: 'Loja', value: 'mdi-store' },
                { title: 'Carrinho', value: 'mdi-cart' },
                { title: 'Facebook', value: 'mdi-facebook' }
            ],
            headers: [
                { title: "ID", key: "id" },
                // { title: "User ID", key: "user_id" },
                { title: "Name", key: "name" },
                { title: "Title", key: "title" },
                { title: "Content", key: "content", align: "right" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
            ],
            defaultPage: {
                id: null,
                name: "",
                title: "",
                content: "",
                //description: "",
                heroTitle: "",
                heroSubtitle: "",
                heroBackgroundColor: "",
                heroImage: "",
                heroButtons: [],
                heroIcon: "",
                carouselImages: [],
                footerText: ""

            },
        };

    },
    watch: {
        editedPage: {
            handler(newVal) {
                if (this.editor && newVal?.content !== undefined) {
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
        this.loadProducts();
        this.loadUploadImages();
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
        async loadProducts() {
            this.loading = true;
            try {
                const response = await api.get('/products');
                return this.products = response.data;
            }
            catch (error) {
                console.log("Error loading products", error);
            }
            finally {
                this.loading = false;
            }
        },
        async loadUploadImages() {
            const res = await api.get('/uploadImages/uploads');
            this.uploadsImages = Array.isArray(res.data) ? res.data : [];
        },
        newPageItem() {
            this.editedPage = { ...this.defaultPage };
            this.dialogPageItem = true;
        },
        openCarouselDialog() {
            this.carouselDialog = true;
        },
        addHeroImage(url) {
            this.editedPage.heroImage = url;
            this.heroImageDialog = false;
        },
        removeHeroImage(index) {
            this.editedPage.heroImage = "";
        },
        openCarouselDialog() {
            this.carouselDialog = true;
        },
        addHeroButton() {
            if(!this.editedPage.heroButtons){
                this.editedPage.heroButtons = [];
            }
            this.editedPage.heroButtons.push({ label: '', url: '' });
        },
        removeHeroButton(index) {
            this.editedPage.heroButtons.splice(index, 1);
        },
        addCarouselImage(url) {
            if (!Array.isArray(this.editedPage.carouselImages)) {
                this.editedPage.carouselImages = [];
            }
            this.editedPage.carouselImages.push(url);
        },
        removeCarouselImage(index) {
            this.editedPage.carouselImages.splice(index, 1);
        },
        editPage(item) {
            this.editedIndex = this.pages.findIndex((page) => page.id === item.id);
            this.editedPage = { ...item };
            this.dialogPageItem = true;
        },
        close() {
            this.dialogPageItem = false;
            this.editedPage = { ...this.defaultPage }; // Mantém um objeto válido
            this.editedIndex = -1;
        },
        async savePage() {
            this.loading = true;
            try {
                const token = localStorage.getItem('access_token');

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
                        title: this.editedPage.title,
                        name: this.editedPage.name,
                        content: this.editedPage.content,
                        heroTitle: this.editedPage.heroTitle,
                        heroSubtitle: this.editedPage.heroSubtitle,
                        heroBackgroundColor: this.editedPage.heroBackgroundColor,
                        heroImage: this.editedPage.heroImage,
                        heroButtons: this.editedPage.heroButtons,
                        carouselImages: this.editedPage.carouselImages,
                        footerText: this.editedPage.footerText,
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
                const token = localStorage.getItem('access_token')
                if (!token) return this.$router.push('/login')

                await api.delete(`/pages/pages/${pageId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                //Remove product from local list
                this.pages = this.pages.filter(page => page.id !== pageId);

                //this.$toast.success('Produto removido com sucesso');
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
.editor-content * {
  outline: none !important;
}
</style>