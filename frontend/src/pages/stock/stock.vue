<template>
    <v-row justify="center">
        <v-col cols="12" md="8" lg="8" xl="6">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Stock Management</h1>
                </v-card-title>

                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct">
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="products" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading products...">
                    
                    <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image" :src="item.image" alt="Product Image" contain 
                            :width="70" :height="70" class="rounded-lg"></v-img>
                        <span v-else>No Image</span>
                    </template>

                    <template v-slot:item.actions="{ item }">
                        <v-icon small class="mr-2" @click.stop="editProduct(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small @click.stop="deleteProduct(item.id)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>
            </v-card>

            <v-dialog v-model="productDialog" max-width="500px">
                <v-card>
                    <v-card-title class="headline">{{ formTitle }}</v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field v-model="editedProduct.name" label="Product Name" outlined dense></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field v-model="editedProduct.quantity" label="Quantity" type="number" outlined dense></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
                        <v-btn color="primary" text @click="saveProduct">Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
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
    data() {
        return {
            loading: false,
            productDialog: false,
            editedIndex: -1,
            editedProduct: { id: null, name: "", quantity: 1 },
            products: [], // Inicializando como array vazio para evitar erros
            headers: [
                { text: "Product Name", value: "name" },
                { text: "Quantity", value: "quantity" },
                { text: "Actions", value: "actions", sortable: false },
            ],
        };
    },
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? "New Product" : "Edit Product";
        }
    },
    created() {
        this.loadProducts();
    },
    methods: {
        async loadProducts() {
            this.loading = true;
            try {
                const response = await api.get("/stock");
                this.products = Array.isArray(response.data) ? response.data : [];
            } catch (error) {
                console.error("Error loading products:", error);
            } finally {
                this.loading = false;
            }
        },
        newProduct() {
            this.editedProduct = { id: null, name: "", quantity: 1 };
            this.editedIndex = -1; // Garante que será um novo produto
            this.productDialog = true;
        },
        editProduct(item) {
            this.editedIndex = this.products.findIndex((p) => p.id === item.id);
            this.editedProduct = { ...item };
            this.productDialog = true;
        },
        async saveProduct() {
            try {
                if (this.editedIndex === -1) {
                    await api.post("/stock", this.editedProduct);
                } else {
                    await api.put(`/stock/${this.editedProduct.id}`, this.editedProduct);
                }
                this.loadProducts();
                this.close();
            } catch (error) {
                console.error("Error saving product:", error);
            }
        },
        async deleteProduct(id) {
            if (!confirm("Are you sure you want to delete this product?")) return;
            try {
                await api.delete(`/stock/${id}`);
                this.loadProducts();
            } catch (error) {
                console.error("Error deleting product:", error);
            }
        },
        close() {
            this.productDialog = false;
            this.editedIndex = -1; // Reseta para evitar problemas ao editar um novo item
        }
    }
};
</script>
