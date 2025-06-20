<template>
    <v-row justify="center">
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
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
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <template v-slot:item.description="{ item }">
                        <span v-if="item.description && item.description.length > 100">
                            {{ item.description.substring(0, 38) }}...
                        </span>
                        <span v-else>
                            {{ item.description }}
                        </span>
                    </template>

                    <!-- 🔹 Slot para categoria -->
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>

                    <!-- 🔹 Slot para ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small color="primary" @click.stop="editProduct(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small color="error" @click.stop="deleteProduct(item.id)">
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
                                        label="Category" item-title="name" item-text="name" item-value="id" outlined
                                        dense></v-select>
                                </v-col>

                                <v-col cols="12" v-if="subcategories.length">
                                    <v-select v-model="editedProduct.subcategory_id" :items="subcategories"
                                        label="Subcategory" item-title="name" item-text="name" item-value="id" outlined
                                        dense></v-select>
                                </v-col>

                                <v-col cols="12">
                                    <v-text-field v-model="editedProduct.name" label="Product Name" outlined
                                        dense></v-text-field>
                                </v-col>

                                <v-col cols="12">
                                    <v-file-input v-model="editedProduct.image" label="Product Image" outlined
                                       show-size dense></v-file-input>
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

                                <v-col cols="6">
                                    <v-text-field v-model="editedProduct.width" label="width(cm)" type="number" outlined
                                        dense></v-text-field>
                                </v-col>
                                <v-col cols="6">
                                    <v-text-field v-model="editedProduct.height" label="Height (cm)" type="number"
                                        outlined dense></v-text-field>
                                </v-col>

                                <v-col cols="6">
                                    <v-text-field v-model="formattedWeight" label="Weight (kg)" type="text"
                                        outlined dense></v-text-field>
                                </v-col>

                                <v-col cols="6">
                                    <v-text-field v-model="editedProduct.length" label="length (cm)" type="number"
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
            : "https://rua11store-catalog-api-lbp7.onrender.com",
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
                width: 1,
                length: 1,
            },
            products: [],
            categories: [],
            headers: [
                // { text: "ID", value: "id", width: "20px", align: "center" },
                { title: "Image", key: "image", sortable: false },
                { title: "Product Name", key: "name", width: "250px" },
                { title: "Product Description", key: "description", width: "250px" },
                { title: "Category", key: "category", width: "200px" },
                { title: "Price", key: "price", width: "120px", align: "right" },
                { title: "Quantity", key: "quantity", width: "120px", align: "right" },
                { title: "Weight", key: "weight", width: "120px", align: "right" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
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
                return this.editedProduct.price !== null && this.editedProduct.price !== undefined
                    ? Number(this.editedProduct.price).toFixed(2).replace(".", ",") // Garante sempre 2 casas decimais
                    : "";
            },
            set(value) {
                let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
                this.editedProduct.price = isNaN(numericValue) ? "0.00" : numericValue.toFixed(2); // Mantém como número
            }
        },
        formattedWeight: {
            get(){
                if(this.editedProduct.weight == null || this.editedProduct.weight == 'undefined') return "";

                return Number(this.editedProduct.weight).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                });
            },
            set(value){
                 const cleaned = value.toString().replace(",", ".").replace(/[^0-9.]/g, "");
                const parsed = parseFloat(cleaned);
                this.editedProduct.weight = isNaN(parsed) ? 0 : parseFloat(parsed.toFixed(2));

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
                console.log(this.products);
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
                formData.append("price", this.editedProduct.price || "0.00");
                formData.append("category_id", this.editedProduct.category_id || "");
                formData.append("subcategory_id", this.editedProduct.subcategory_id || "");
                formData.append("quantity", this.editedProduct.quantity || 1);
                formData.append("imagem", this.editedProduct.image || "");
                formData.append('width', this.editedProduct.width || "");
                formData.append('height', this.editedProduct.height || "");
                formData.append('weight', this.editedProduct.weight || "");
                formData.append('length', this.editedProduct.length || "");

                const config = {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "multipart/form-data",
                    },
                };

                let response;
                if (this.editedIndex === -1) {
                    response = await api.post("/products", formData, config);
                    if (response.data.product) {
                        response.data.product.image_url = this.getProductImage(
                            response.data.product.image_path,
                            response.data.product.id
                        );
                    }
                    this.products.push(response.data.product);
                } else {
                    response = await api.put(`/products/${this.editedProduct.id}`, formData, config);
                    Object.assign(this.products[this.editedIndex], response.data.product);
                }

                this.close();
            } catch (error) {
                console.error("Error saving product:", error);
            }
        },
        getProductImage(imagePath, productId = null) {
            // Imagem padrão se não houver caminho
            if (!imagePath) return "https://via.placeholder.com/300";

            // Se já for URL completa (http ou https)
            if (imagePath.startsWith('http')) {
                return imagePath.replace('http://', 'https://'); // Força HTTPS
            }

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
        async deleteProduct(productId) {
            if (!confirm("Tem certeza que deseja remover este produto permanentemente ?")) return;

            try {
                const token = localStorage.getItem('user_token')
                if (!token) return this.$router.push('/login')

                await api.delete(`/products/${productId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                //Remove product from local list
                this.products = this.products.filter(p => p.id !== productId);

                this.$toast.success('Produto removido com sucesso');
            }
            catch (error) {
                console.log("Error deleting product:", error);
                this.$toast.error("Erro ao excluir produto");
            }
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