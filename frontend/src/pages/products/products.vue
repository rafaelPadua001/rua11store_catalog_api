<template>
    <v-row justify="center">
        <v-col cols="12" md="8" lg="8" xl="6">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Products Management</h1>
                </v-card-title>

                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct">
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="products" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading products...">
                    <!-- 🔹 Slot para exibir imagens -->
                    <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path)" alt="Imagem do Produto"
                            contain max-width="60" max-height="60" class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <!-- 🔹 Slot para categoria -->
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>

                    <!-- 🔹 Slot para ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small class="mr-2" @click.stop="editProduct(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small @click.stop="deleteProduct(item)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>
            </v-card>

            <!-- Modal para Adicionar/Editar Produto -->
            <v-dialog v-model="productDialog" max-width="500px">
                <v-card>
                    <v-card-title class="headline">{{ formTitle }}</v-card-title>
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-select v-model="editedProduct.category_id" :items="mainCategories"
                                        label="Category" item-text="name" item-value="id" outlined dense></v-select>
                                </v-col>

                                <v-col cols="12" v-if="subcategories.length">
                                    <v-select v-model="editedProduct.subcategory_id" :items="subcategories"
                                        label="Subcategory" item-text="name" item-value="id" outlined dense></v-select>
                                </v-col>

                                <v-col cols="12">
                                    <v-text-field v-model="editedProduct.name" label="Product Name" outlined
                                        dense></v-text-field>
                                </v-col>

                                <v-col cols="12">
                                    <v-file-input v-model="editedProduct.image" label="Product Image" outlined
                                        dense></v-file-input>
                                </v-col>

                                <v-col cols="12">
                                    <v-textarea v-model="editedProduct.description" label="Description" outlined
                                        dense></v-textarea>
                                </v-col>

                                <v-col cols="6">
                                    <v-text-field v-model="formattedPrice" label="Price" outlined dense
                                        @input="updatePrice"></v-text-field>
                                </v-col>

                                <v-col cols="6">
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
//   import { directive as mask } from "v-mask";


const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
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
            editedProduct: null, // Inicialmente nulo para evitar erros de acesso
            defaultProduct: {
                id: null,
                name: "",
                category_id: null,
                subcategory_id: null,
                image: null,
                description: "",
                price: 0,
                quantity: 1,
            },
            products: [],
            categories: [],
            headers: [
                { text: "ID", value: "id", width: "80px", align: "center" },
                { text: "Image", value: "image", width: "100px", align: "center", sortable: false },
                { text: "Product Name", value: "name", width: "250px" },
                { text: "Category", value: "category", width: "200px" },
                { text: "Price", value: "price", width: "120px", align: "right" },
                { text: "Quantity", value: "quantity", width: "120px", align: "right" },
                { text: "Actions", value: "actions", width: "120px", align: "center", sortable: false },
            ],
        };
    },
    computed: {
        mainCategories() {
            return this.categories.filter((c) => !c.is_subcategory);
        },
        subcategories() {
            if (!this.editedProduct || !this.editedProduct.category_id) return [];
            return this.categories.filter((c) => c.is_subcategory && c.parent_id === this.editedProduct.category_id);
        },
        formTitle() {
            return this.editedIndex === -1 ? "New Product" : "Edit Product";
        },
        formattedPrice: {
            get() {
                return this.editedProduct.price
                    ? new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(this.editedProduct.price)
                    : "";
            },
            set(value) {
                let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
                this.editedProduct.price = isNaN(numericValue) ? 0 : numericValue;
            }
        }
    },
    created() {
        this.loadCategories();
        this.loadProducts();
    },
    methods: {
        async loadCategories() {
            this.loading = true;
            try {
                const response = await api.get("/categories/");
                this.categories = response.data;
            } catch (error) {
                console.error("Error loading categories:", error);
            } finally {
                this.loading = false;
            }
        },
        async loadProducts() {
            this.loading = true;
            try {
                const response = await api.get("/products");
                this.products = response.data;
            } catch (error) {
                console.error("Error loading products:", error);
            } finally {
                this.loading = false;
            }
        },
        newProduct() {
            this.editedProduct = { ...this.defaultProduct };
            this.productDialog = true;
        },
        editProduct(item) {
            this.editedIndex = this.products.findIndex((p) => p.id === item.id);
            this.editedProduct = { ...item };
            this.productDialog = true;
        },
        async saveProduct() {
            try {
                if (!this.editedProduct) {
                    console.error("Erro: editedProduct está null");
                    return;
                }

                const token = localStorage.getItem("user_token");
                if (!token) return this.$router.push("/login");

                const formData = new FormData();
                formData.append("name", this.editedProduct.name || ""); // Evita erro
                formData.append("description", this.editedProduct.description || "");
                formData.append("price", this.editedProduct.price || 0);
                formData.append("category_id", this.editedProduct.category_id || "");
                formData.append("subcategory_id", this.editedProduct.subcategory_id || "");
                formData.append("quantity", this.editedProduct.quantity || 1);
                formData.append("imagem", this.editedProduct.image || "");

                const config = {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "multipart/form-data",
                    },
                };

                let response;
                if (this.editedIndex === -1) {
                    response = await api.post("/products", formData, config);
                    this.products.push(response.data.product);
                } else {
                    response = await api.put(`/products/${this.editedProduct.id}`, formData, config);
                    console.log(response);
                    Object.assign(this.products[this.editedIndex], response.data.product);
                }

                this.close();
            } catch (error) {
                console.error("Error saving product:", error);
            }
        },
        getProductImage(imagePath) {
            if (!imagePath) return "https://via.placeholder.com/300"; // Imagem padrão maior
            
            // Se já for uma URL completa (http ou https)
            if (imagePath.startsWith('http')) return imagePath;
            
            // Para ambiente de desenvolvimento (local)
            if (process.env.NODE_ENV === 'development') {
                const localBaseUrl = "http://localhost:5000";
                console.log(localBaseUrl);
                return `${localBaseUrl}/uploads/${imagePath.split('/').pop()}`;
            }
            
            // Para produção no Railway
            const railwayBaseUrl = import.meta.env.VITE_RAILWAY_URL || "https://rua11storecatalogapi-production.up.railway.app";
            return `${railwayBaseUrl}/uploads/${imagePath.split('/').pop()}`;
        },
        close() {
            this.productDialog = false;
            this.editedProduct = { ...this.defaultProduct }; // Mantém um objeto válido
            this.editedIndex = -1;
        },
        getCategoryName(id) {
            const category = this.categories.find((c) => c.id === id);
            return category ? category.name : "Unknown";
        },
    },
};
</script>