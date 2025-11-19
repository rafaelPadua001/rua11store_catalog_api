<template>
    <v-card class="pa-4 text-center">
        <v-toolbar flat color="transparent">
            <v-toolbar-title class="headline">{{ formTitle }}</v-toolbar-title>

            <v-btn icon @click="close">
                <v-icon>mdi-close</v-icon>
            </v-btn>

        </v-toolbar>
        <v-card-text>
            <v-row dense>
                <v-subheader class="text-left">Informações Básicas</v-subheader>
                <v-divider class="mb-3"></v-divider>
                <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="editedProduct.name" label="Product Name" outlined dense>
                    </v-text-field>
                </v-col>
            </v-row>

            <v-row dense>
                <v-subheader class="text-left">Midias</v-subheader>
                <v-divider class="mb-3"></v-divider>
                <v-col cols="12" md="4" sm="6">
                    <v-file-input v-model="editedProduct.thumbnail" label="Product Thumbnail" outlined show-size dense
                        prepend-icon="mdi-image" accept="image/*" @change="thumbnailPreview">
                    </v-file-input>
                    <v-img v-if="thumbnailImage" :src="thumbnailImage" max-height="200" class="rounded mt-1"
                        aspect-ratio="1">
                        <v-btn v-if="thumbnailImage" icon class="position-absolute mt-2" color="black" size="x-small"
                            @click="removeThumbnail" style="top: 5px; right: 5px;">
                            <v-icon end>mdi-close</v-icon>
                        </v-btn>
                    </v-img>
                    <v-img v-else="editedIndex >= 1" :src="editedProduct.thumbnail_path" max-height="200"
                        class="rounded mt-1" aspect-ratio="1">
                        <v-btn v-if="editedIndex >= 1" icon class="position-absolute mt-2" color="black" size="x-small"
                            @click="removeThumbnail" style="top: 5px; right: 5px;">
                            <v-icon end>mdi-close</v-icon>
                        </v-btn>
                    </v-img>

                </v-col>
                <v-col cols="12" md="4" sm="6">
                    <v-file-input v-model="editedProduct.images" label="Product Images" outlined show-size dense
                        multiple prepend-icon="mdi-image-multiple" accept="image/*" @change="imagesPreview" />

                    <!-- Mostrar apenas as imagens selecionadas no formulário -->
                    <v-row v-if="imagesPreviews.length > 0">
                        <v-col v-for="(img, index) in imagesPreviews" :key="'preview-' + index" cols="6" md="4"
                            class="position-relative">
                            <v-img :src="img" max-height="200" class="rounded mt-1" aspect-ratio="1" />
                            <v-btn icon size="x-small" color="black" class="position-absolute mt-2"
                                style="top: 5px; right: 5px;" @click="removeImage(index)">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>

                    <!-- Mostrar apenas as imagens já salvas no banco -->
                    <v-row v-else-if="Array.isArray(editedProduct.images) && editedProduct.images.length > 0">
                        <v-col v-for="(img, index) in editedProduct.images" :key="'saved-' + index" cols="6" md="4"
                            class="position-relative">
                            <v-img :src="typeof img === 'string' ? img : img.image_path" max-height="200"
                                class="rounded mt-1" aspect-ratio="1" />
                            <v-btn icon size="x-small" color="black" class="position-absolute mt-2"
                                style="top: 5px; right: 5px;" @click="removeImage(index)">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-col>

                <v-col cols="12" md="4" sm="6">
                    <v-file-input v-model="editedProduct.video" label="Product Video" outlined show-size dense
                        prepend-icon="mdi-video" accept="video/*" />

                    <!-- Se for vídeo novo (preview do FileInput) -->
                    <v-row v-if="videoPreview">
                        <v-col cols="auto">
                            <video :src="videoPreview" controls style="max-width: 100%; margin-top: 10px;"></video>
                            <v-btn icon size="x-small" color="black" class="mt-2" @click="removeVideo"
                                style="top: 5px; right: 5px;">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>

                    <!-- Se for vídeo vindo do banco -->
                    <v-row v-else-if="editedProduct.video">
                        <v-col cols="auto">
                            <video
                                :src="typeof editedProduct.video === 'string' ? editedProduct.video : editedProduct.video.video_path"
                                controls style="max-width: 100%; margin-top: 10px;"></video>
                            <v-btn icon size="x-small" color="black" class="mt-2" @click="removeVideo"
                                style="top: 5px; right: 5px;">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-col>

            </v-row>

            <v-row dense>
                <v-subheader class="text-left">Categoria</v-subheader>
                <v-divider class="mb-3"></v-divider>
                <v-col cols="12" md="6" sm="6">
                    <v-select v-model="editedProduct.category_id" :items="mainCategories" label="Category"
                        item-title="name" item-text="name" item-value="id" outlined dense></v-select>
                </v-col>

                <v-col cols="12" md="6" sm="6">
                    <v-select v-model="editedProduct.subcategory_id" :items="subcategories" label="Subcategory"
                        item-title="name" item-text="name" item-value="id" outlined dense></v-select>
                </v-col>

            </v-row>

            <v-row dense>
                <v-subheader class="text-left">Variations</v-subheader>
                <v-divider></v-divider>

                <v-col cols="12" md="6">
                    <div v-for="(size, index) in editedProduct.sizes" :key="'size-' + index"
                        class="d-flex mb-2 align-center">
                        <!-- Nome do tamanho -->
                        <v-text-field v-model="size.value" label="Tamanho" outlined dense class="me-2"
                            append-icon="mdi-close" @click:append="removeSize(index)"></v-text-field>

                        <!-- Quantidade -->
                        <v-text-field v-model.number="size.quantity" label="Quantidade" type="number" outlined dense
                            style="max-width: 120px;"></v-text-field>
                    </div>

                    <v-btn text small color="primary" @click="addSize">Adicionar Tamanho</v-btn>
                </v-col>

                <v-col cols="12" md="6">
                    <div v-for="(color, index) in editedProduct.colors" :key="'color-' + index"
                        class="mb-2 d-flex align-center">
                        <!-- Campo de cor -->
                        <v-menu v-model="colorMenu[index]" :close-on-content-click="false" max-width="290px" offset-y>
                            <template #activator="{ props }">
                                <v-text-field v-bind="props" v-model="editedProduct.colors[index].value" label="Cor"
                                    outlined dense readonly append-icon="mdi-chevron-down">

                                    <template #prepend-inner>
                                        <div :style="{
                                            backgroundColor: editedProduct.colors[index].value,
                                            width: '20px',
                                            height: '20px',
                                            borderRadius: '50%',
                                            border: '1px solid #ccc'
                                        }"></div>
                                    </template>
                                </v-text-field>
                            </template>

                            <!-- Color Picker -->
                            <v-color-picker v-model="editedProduct.colors[index].value" flat></v-color-picker>
                        </v-menu>

                        <!-- Quantidade -->
                        <v-text-field v-model.number="editedProduct.colors[index].quantity" label="Quantidade"
                            type="number" outlined dense style="max-width: 120px;"></v-text-field>
                        <!-- Botão de remover -->
                        <v-btn variant="plain" size="x-small" color="red" @click="removeColor(index)" icon="mdi-close">

                        </v-btn>
                    </div>

                    <v-btn text small color="primary" @click="addColor">Adicionar Cor</v-btn>
                </v-col>

            </v-row>

            <v-row dense>
                <v-subheader class="text-left">Descrição</v-subheader>
                <v-divider class="mb-3"></v-divider>
                <v-col cols="12">
                    <v-textarea v-model="editedProduct.description" label="Description" outlined dense>
                    </v-textarea>
                </v-col>
            </v-row>

            <v-row dense>
                <v-subheader class="text-left">Estoque</v-subheader>
                <v-divider class="mb-3"></v-divider>
                <v-col cols="6">
                    <v-text-field v-model="formattedPrice" label="Price" outlined dense
                        @input="updatePrice"></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field v-model="editedProduct.quantity" label="Quantity" type="number" outlined
                        dense></v-text-field>
                </v-col>
            </v-row>

            <v-row dense>
                <v-subheader class="text-left">Dimensões</v-subheader>
                <v-divider class="mb-3"></v-divider>
                <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="editedProduct.width" label="width(cm)" type="number" outlined
                        dense></v-text-field>
                </v-col>
                <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="editedProduct.height" label="Height (cm)" type="number" outlined
                        dense></v-text-field>
                </v-col>
            </v-row>
            <v-row dense>
                <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="formattedWeight" label="Weight (kg)" type="text" outlined
                        dense></v-text-field>
                </v-col>

                <v-col cols="12" md="4" sm="6">
                    <v-text-field v-model="editedProduct.length" label="length (cm)" type="number" outlined
                        dense></v-text-field>
                </v-col>
            </v-row>

            <v-row dense>
                <v-subheader class="text-left">SEO</v-subheader>
                <v-col cols="12">

                    <v-divider class="mb-3"></v-divider>
                </v-col>

                <v-col cols="12" md="6">
                    <v-text-field v-model="editedProduct.seo.meta_title" label="Meta Title" outlined
                        dense></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                    <v-text-field v-model="editedProduct.seo.slug" label="Slug (URL)" outlined dense></v-text-field>
                </v-col>

                <v-col cols="12">
                    <v-textarea v-model="editedProduct.seo.meta_description" label="Meta Description" outlined dense
                        rows="2" auto-grow></v-textarea>
                </v-col>

                <v-col cols="12">
                    <v-text-field v-model="editedProduct.seo.keywords" label="Keywords (separadas por vírgula)" outlined
                        dense></v-text-field>
                </v-col>
            </v-row>


        </v-card-text>
        <v-card-actions>
            <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
            <v-btn color="primary" text @click="saveProduct">Save</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
import { ref, watch } from 'vue';
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
    props: {
        editedProduct: Object,
        categories: Array,
        mainCategories: Array,
        subcategories: Array,
        formTitle: String,
    },
    emits: ['close', 'save-product'],
    data() {
        return {
            loading: false,
            productDialog: false,
            editedIndex: -1,
            products: [],
            thumbnailImage: null,
            imagesPreviews: [],
            videoPreview: null,
            colorMenu: [],
        };
    },
    watch: {
        'editedProduct.thumbnail': {
            handler(newFile) {
                console.log(newFile);
                if (newFile instanceof File) {
                    this.thumbnailImage = URL.createObjectURL(newFile);
                } else if (Array.isArray(newFile) && newFile[0] instanceof File) {
                    this.thumbnailImage = URL.createObjectURL(newFile[0]);
                } else {
                    this.thumbnailImage = null;
                }
            },
            immediate: true
        },
        'editedProduct.images': {
            handler(newFiles, oldFiles) {
                if (Array.isArray(this.imagesPreviews)) {
                    this.imagesPreviews.forEach(url => URL.revokeObjectURL(url));

                }
                if (Array.isArray(newFiles) && newFiles.length > 0) {
                    this.imagesPreviews = newFiles.map(file => {
                        if (file instanceof File) {
                            return URL.createObjectURL(file)
                        }
                        else if (typeof file == 'string') {
                            return file;
                        }
                        return null;
                    }).filter(Boolean); //remove null values
                }
                else {
                    this.imagesPreviews = [];
                }
            },
            immediate: true
        },
        'editedProduct.video': {
            handler(newFile) {
                if (newFile instanceof File) {
                    if (this.videoPreview) {
                        URL.revokeObjectURL(this.videoPreview); // Limpa o URL anterior
                    }
                    this.videoPreview = URL.createObjectURL(newFile);

                }
                else {
                    if (this.videoPreview) {
                        URL.revokeObjectURL(this.videoPreview); // Limpa o URL anterior
                    }
                    this.videoPreview = null;
                }
            },
            immediate: true
        }
    },
    computed: {
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
        if (!this.editedProduct.sizes) {
            this.editedProduct.sizes = [];
        }
        else {
            this.editedProduct.sizes = this.editedProduct.sizes.map(s => {
                if (typeof s === 'string') return { name: s, quantity: 0 };
                return { ...s };
            });
        }
        if (!this.editedProduct.colors) {
            this.editedProduct.colors = [];
        } else {
            this.editedProduct.colors = this.editedProduct.colors.map(s => {
                if (typeof s === 'string') return { value: s, quantity: 0 }; // ✅ usar value
                return { value: s.value || s.name || '', quantity: s.quantity || 0 };
            });
        }
    },
    methods: {
        editProduct(item) {
            this.editedIndex = this.products.findIndex((p) => p.id === item.id);

            //sizes and colors is array
            const sizes = Array.isArray(item.sizes)
                ? item.sizes.map(s => (typeof s === 'string' ? { name: s, quantity: 0 } : {
                    name: s.name || '',
                    quantity: s.quantity || 0
                }))
                : [];

            const colors = Array.isArray(item.colors)
                ? item.colors.map(c => (typeof c === 'string' ? { value: c, quantity: 0 } : {
                    value: c.value || c.name || '',
                    quantity: c.quantity || 0
                }))
                : [];



            this.editedProduct = {
                ...item,
                sizes,
                colors,
                seo: item.seo ? { ...item.seo } : { meta_title: "", meta_description: "", slug: "", keywords: "" }
            };

            this.colorMenu = colors.map(() => false);
            this.productDialog = true;
        },
        async saveProduct() {
            this.$emit('save-product')
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
        close() {
            this.$emit('close');
        },
        getCategoryName(id) {
            const category = this.categories.find((c) => c.id === id);
            return category ? category.name : "Unknown";
        },
        addSize() {
            this.editedProduct.sizes.push({ name: '', quantity: 0 });
        },
        removeSize(index) {
            this.editedProduct.sizes.splice(index, 1);
        },
        addColor() {
            this.editedProduct.colors.push({ value: '', quantity: 0 }); // ✅ value, não name
            this.colorMenu.push(false);
        },

        removeColor(index) {
            this.editedProduct.colors.splice(index, 1);
            this.colorMenu.splice(index, 1);
        },
        removeThumbnail() {
            this.editedProduct.thumbnail = null;
            this.thumbnailImage = null;
        },
        removeImage(index) {
            const fileList = this.editedProduct.images;

            // Remove o arquivo da lista
            if (Array.isArray(fileList)) {
                fileList.splice(index, 1);
            }

            // Remove a URL do preview
            if (Array.isArray(this.imagesPreviews)) {
                URL.revokeObjectURL(this.imagesPreviews[index]); // limpa da memória
                this.imagesPreviews.splice(index, 1);
            }
        },
        removeVideo() {
            this.editedProduct.video = null;
            if (this.videoPreview) {
                URL.revokeObjectURL(this.videoPreview);
                this.videoPreview = null;
            }
        }
    },
};

</script>