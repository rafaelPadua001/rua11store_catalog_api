<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>Products Management</h5>
                </v-card-title>

                <v-divider></v-divider>

                <v-card-actions class="d-flex justify-end mb-0">
                    <v-btn color="primary" @click="newProduct">
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="products" :items-per-page="20" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading products...">
                    <!-- 🔹 Slot para exibir imagens -->
                    <template v-slot:item.thumbnail_path="{ item }">
                        <v-img v-if="item.thumbnail_path || (item.image_paths && item.image_paths.length > 0)"
                            :src="getProductImage(item.thumbnail_path || item.image_paths[0], item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="60" min-height="30"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <!--<template v-slot:item.description="{ item }">
                        <span v-if="item.description && item.description.length > 100">
                            {{ item.description.substring(0, 38) }}...
                        </span>
                        <span v-else>
                            {{ item.description }}
                        </span>
                    </template> -->

                    <!-- 🔹 Slot para categoria -->
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>

                    <!-- slot para price-->
                    <template v-slot:item.price="{ item }">
                        <span v-if="item && item.price">R$ {{ item.price }}</span>
                    </template>

                    <!-- 🔹 Slot para ações -->
                    <template v-slot:item.actions="{ item }">
                        <router-link v-if="item.seo" :to="`/products/productView/${item.seo.slug}`">
                            <v-icon small color="primary">mdi-eye</v-icon>
                        </router-link>

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
            <v-dialog v-model="productDialog" max-width="600" fullscreen>
                <ProductForm :edited-product="editedProduct" :categories="categories" :main-categories="mainCategories"
                    :subcategories="subcategories" :form-title="formTitle" @close="close" @save-product="saveProduct" />

            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
import axios from "axios";
import ProductForm from "./ProductForm.vue";
//   import { directive as mask } from "v-mask";


const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    components: {
        ProductForm
    },
    data() {
        return {
            loading: false,
            productDialog: false,
            editedIndex: -1,
            editedProduct: {
                id: null,
                name: '',
                description: '',
                price: '',
                category_id: null,
                subcategory_id: null,
                image_path: '',
                quantity: 0,
                width: 0,
                height: 0,
                weight: 0,
                length: 0,
                user_id: null,
                seo: {
                    meta_title: '',
                    meta_description: '',
                    slug: '',
                    keywords: ''
                }
            },

            // Inicialmente nulo para evitar erros de acesso
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
                seo: {  // <-- Aqui
                    meta_title: '',
                    meta_description: '',
                    slug: '',
                    keywords: ''
                }
            },
            products: [],
            categories: [],
            headers: [
                // { text: "ID", value: "id", width: "20px", align: "center" },
                { title: "Image", key: "thumbnail_path", sortable: false, width: "150px" },
                { title: "Product Name", key: "name", width: "150px" },
                // { title: "Product Description", key: "description", width: "150px" },
                { title: "Category", key: "category", width: "100px" },
                { title: "Price", key: "price", width: "120px", align: "right" },
                // { title: "Quantity", key: "quantity", width: "120px", align: "right" },
                //  { title: "Weight", key: "weight", width: "120px", align: "right" },
                { title: "Actions", key: "actions", width: "100px", align: "center", sortable: false },
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
            get() {
                if (this.editedProduct.weight == null || this.editedProduct.weight == 'undefined') return "";

                return Number(this.editedProduct.weight).toLocaleString("en-US", {
                    minimumFractionDigits: 3,
                    maximumFractionDigits: 3,
                });
            },
            set(value) {
                const cleaned = value.toString().replace(",", ".").replace(/[^0-9.]/g, "");
                const parsed = parseFloat(cleaned);
                this.editedProduct.weight = isNaN(parsed) ? 0 : parseFloat(parsed.toFixed(3));

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
                //  console.log(this.products);
            } catch (error) {
                console.error("Error loading products:", error);
            } finally {
                this.loading = false;
            }
        },
        newProduct() {
            this.editedProduct = { ...this.defaultProduct, seo: { ...this.defaultProduct.seo } };
            this.productDialog = true;
        },
        editProduct(item) {
            this.editedIndex = this.products.findIndex((p) => p.id === item.id);
            this.editedProduct = { ...item, seo: item.seo ? { ...item.seo } : { meta_title: "", meta_description: "", slug: "", keywords: "" } };
            this.productDialog = true;
        },
        async saveProduct() {
            try {
                if (!this.editedProduct) {
                    console.error("Erro: editedProduct está null");
                    return;
                }

                const token = localStorage.getItem("access_token");
                if (!token) return this.$router.push("/login");


                const formData = new FormData();
                formData.append("name", this.editedProduct.name || ""); // Evita erro
                formData.append("description", this.editedProduct.description || "");
                formData.append("price", this.editedProduct.price || "0.00");
                formData.append("category_id", this.editedProduct.category_id || "");
                formData.append("subcategory_id", this.editedProduct.subcategory_id || "");
                formData.append('sizes', JSON.stringify(this.editedProduct.sizes || ''));
                formData.append('colors', JSON.stringify(this.editedProduct.colors || ''));
                formData.append("quantity", this.editedProduct.quantity || 1);
                formData.append("thumbnail", this.editedProduct.thumbnail || "");
                if (Array.isArray(this.editedProduct.images)) {
                    this.editedProduct.images.forEach((file) => {
                        if (file instanceof File) {
                            formData.append("images", file);
                        }
                    });
                }
                formData.append("video", this.editedProduct.video || "");
                formData.append('width', this.editedProduct.width || "");
                formData.append('height', this.editedProduct.height || "");
                formData.append('weight', this.editedProduct.weight || "");
                formData.append('length', this.editedProduct.length || "");
                formData.append('length', this.editedProduct.length || "");
                formData.append("meta_title", this.editedProduct.seo?.meta_title || "");
                formData.append("meta_description", this.editedProduct.seo?.meta_description || "");
                formData.append("slug", this.editedProduct.seo?.slug || "");
                formData.append("keywords", this.editedProduct.seo?.keywords || "");



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

                    const updated = response.data.product;
                    const target = this.products[this.editedIndex];

                    // Atualiza somente o que veio do backend (não sobrescreve as variações!)
                    for (const key in updated) {
                        target[key] = updated[key];
                    }

                    // Mantém as cores/tamanhos
                    target.colors = [...this.editedProduct.colors];
                    target.sizes = [...this.editedProduct.sizes];
                    target.variations = { ...this.editedProduct.variations };

                    console.log("FINAL PRODUCT =>", target);
                }


                this.close();
            } catch (error) {
                console.log("Error saving product:", error);
            }
        },
        getProductImage(imagePath, productId = null) {
            // Imagem padrão se não houver caminho
            if (!imagePath) return "https://via.placeholder.com/300";


            return imagePath.startsWith('http')
                ? imagePath.replace('http://', 'https://') // garante HTTPS
                : imagePath;
        },
        async deleteProduct(productId) {
            if (!confirm("Tem certeza que deseja remover este produto permanentemente ?")) return;

            try {
                const token = localStorage.getItem('access_token')
                if (!token) return this.$router.push('/login')

                await api.delete(`/products/${productId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                //Remove product from local list
                this.products = this.products.filter(p => p.id !== productId);

                console.log('Produto removido com sucesso');
            }
            catch (error) {
                console.log("Error deleting product:", error);
                //   this.$toast.error("Erro ao excluir produto");
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