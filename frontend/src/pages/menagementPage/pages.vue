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
           
                <v-data-table :headers="headers" :items="pages" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading pages...">
                    <!-- Exibe imagens de produtos -->
                    <template v-slot:item.title="{ item }">
                        <span>{{ item.title }}</span>
                    </template>
                     <template v-slot:item.content="{ item }">
                        <span>{{ item.content }}</span>
                    </template>

                     <template v-slot:item.actions="{ item }">
                        <v-icon small color="primary" @click.stop="editProduct(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small color="error" @click.stop="deleteProduct(item.id)">
                            mdi-delete
                        </v-icon>
                    </template>

                </v-data-table>

                <v-dialog v-model="dialogPageItem" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">New Page</span>
                        </v-card-title>
                        <divider></divider>
                        <hr>

                        <v-card-content>
                            <v-container>
                                <v-form @submit.prevent="savePage">
                                    <v-text-field v-model="editedPage.title" label="Título" required />
                                    <v-textarea v-model="editedPage.content" label="Conteúdo" required />
                                    <v-btn type="submit" color="primary">Salvar</v-btn>
                                </v-form>
                            </v-container>
                        </v-card-content>

                        <v-card-actions>
                            <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
                            <v-btn color="primary" text @click="saveProduct">Save</v-btn>
                        </v-card-actions>


                    </v-card>
                </v-dialog>
            </v-card>


        </v-col>
    </v-row>
</template>

<script>
import axios from "axios";

const api = axios.create({
    baseURL: window.location.hostname === "localhost"
        ? "http://localhost:5000"
        : "https://rua11storecatalogapi-production.up.railway.app",
    headers: { "Content-Type": "application/json" },
});

export default {
    props: ['id'],
    data() {
        return {
            loading: false,
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
                { title: "Title", key: "title" },
                { title: "Content", key: "content", align: "right" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
            ],
            isPaymentButtonPayTagDisabled: true,
            isCheckitemButton: true,
            dialogPageItem: false,
            defaultProduct: {
                id: null,
                title: "",
                description: "",

            },
        };

    },
    // computed: {
    //    
    // },
    async created() {
        this.loadpages();
        if (this.id) {
            const res = await api.get(`/pages/${this.id}`);
            this.page = await res.json();
        }
    },
    methods: {
        async loadpages(){
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
                        title: this.editedPage.title,
                        content: this.editedPage.content
                    }, config);
                    this.pages.push(response.data.page);
                } else {
                    response = await api.put(`/pages/${this.editedPage.id}`, this.editedPage, config);
                    Object.assign(this.pages[this.editedIndex], response.data.page);
                }
                this.close();
            } catch (error) {
                console.error("Error saving page:", error);
            }
        },

    }

};
</script>
