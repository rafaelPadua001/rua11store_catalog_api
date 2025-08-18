<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>Stock Management</h5>
                </v-card-title>
                <v-divider></v-divider>

                <v-data-table :headers="headers" :items="stocks" :items-per-page="10" class="elevation-1" item-key="id"
                    fixed-header height="500" :loading="loading" loading-text="Loading stock...">
                
                    <template v-slot:item.thumbnail_path="{ item }">
                        <v-img v-if="item.product.thumbnail_path" :src="getProductImage(item.product.thumbnail_path, item.id) " alt="Product Image" contain :width="70" :height="70" 
                            class="rounded-lg"></v-img>
                        <span v-else>No Image</span>
                    </template>

                    <template v-slot:item.product_price="{item}">
                        R$ {{ item.product.price }}
                    </template>
                    
                    <template v-slot:item.actions="{ item }">
                        <v-icon small @click.stop="deleteStock(item.id)" color="error">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>
            </v-card>

            <v-dialog v-model="stockDialog" max-width="500px">
                <v-card>
                    <v-card-title class="headline">{{ formTitle }}</v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field v-model="editedProduct.name" label="Product Name" outlined
                                        dense></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field v-model="editedProduct.quantity" label="Quantity" type="number"
                                        outlined dense></v-text-field>
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
        : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    data() {
        return {
            loading: false,
            stockDialog: false,
            editedIndex: -1,
            editedStock: { id: null, name: "", quantity: 1 },
            stocks: [],
            headers: [
                { title: "Product Image", key: "thumbnail_path", sortable: false  },
                { title: "Product Name", key: "product_name" },
                { title: "Variations", key: "variations" },
                { title: "Quantity", key: "product_quantity" },
                { title: "Price", key: "product_price" },
                { title: "Actions", key: "actions", sortable: false },
            ],
        };
    },
    created() {
        this.loadStocks();
    },
    methods: {
        async loadStocks() {
            this.loading = true;
            try {
                const response = await api.get("/stock");
                this.stocks = Array.isArray(response.data) ? response.data : [];
            } catch (error) {
                console.error("Error loading products:", error);
            } finally {
                this.loading = false;
            }
        },
        getProductImage(imagePath, productId = null) {
            
            // Imagem padrão se não houver caminho
            if (!imagePath) return "https://via.placeholder.com/300";

            // Se já for URL completa (http ou https)
            if (imagePath.startsWith('http')) {
                return imagePath.replace('http://', 'https://'); // Força HTTPS
            }

            return imagePath.startsWith('http')
            ? imagePath.replace('http://', 'https://') // garante HTTPS
            : imagePath;

            // Define a base URL conforme o ambiente
            const baseUrl = window.location.hostname === 'localhost'
                ? 'http://localhost:5000'
                : 'https://rua11store-catalog-api-lbp7.onrender.com';

            // Extrai o nome do arquivo (última parte do caminho)
            const filename = imagePath.split('/').pop();

            // Obtém o nome do produto de forma segura
            let productName = 'produto';

            // Se tiver productId, busca na lista de produtos
            if (productId) {
                const product = this.products.find(p => p.id === productId);
                if (product?.name) {
                    productName = product.name.replace(/\s+/g, '_').toLowerCase();
                }
            }
            // Se estiver editando, usa o editedProduct
            else if (this.editedProduct?.name) {
                productName = this.editedProduct.name.replace(/\s+/g, '_').toLowerCase();
            }
           
            return `${baseUrl}/${imagePath}`;
        },
        async deleteStock(id) {
            if (!confirm("Are you sure you want to delete this product?")) return;
            try {
                await api.delete(`/stock/${id}`);
                this.loadStocks();
            } catch (error) {
                console.error("Error deleting product:", error);
            }
        },
        close() {
            this.stockDialog = false;
            this.editedIndex = -1;
        }
    }
};
</script>
