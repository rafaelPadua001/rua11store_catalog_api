<template>
    <v-row justify="center">
        <v-col cols="12" md="8" lg="8" xl="6">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Delivery Management</h1>
                </v-card-title>

                <!-- <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct" disabled>
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions> -->

                <v-data-table :headers="headers" :items="deliveries" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading deliveries...">
                    <!-- Exibe imagens de produtos -->
                    <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <!-- Exibe a descrição do produto -->
                    <template v-slot:item.description="{ item }">
                        <span v-if="item.description && item.description.length > 100">
                            {{ item.description.substring(0, 38) }}...
                        </span>
                        <span v-else>
                            {{ item.description }}
                        </span>
                    </template>

                    <!-- Exibe a categoria -->
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>

                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small @click.stop="deleteProduct(item.id)">
                            mdi-tab
                        </v-icon>
                        <v-icon small @click.stop="deleteProduct(item.id)">
                            mdi-bookmark
                        </v-icon>
                        <v-icon small @click.stop="deleteProduct(item.id)">
                            mdi-delete
                        </v-icon>
                        
                    </template>
                </v-data-table>
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
    data() {
        return {
            loading: false,
            deliveries: [],
            headers: [
                { text: "ID", value: "id" },
                { text: "User ID", value: "user_id" },
                { text: "Recipient Name", value: "recipient_name" },
                { text: "Street", value: "street", align: "right" },
                { text: "number", value: "number" },
                { text: "complement", value: "complement" },
                { text: "city", value: "city" },
                { text: "state", value: "state" },
                { text: "zipcode", value: "zip_code" },
                { text: "bairro", value: "bairro" },
                { text: "country", value: "country" },
                { text: "phone", value: "phone" },
                { text: "Email", value: "userEmail" },
                { text: "Price", value: "price" },
                // { text: "Delivery", value: "delivery_id" },
                { text: "Actions", value: "actions", width: "120px", align: "center", sortable: false },
            ],
        };
    },
    computed: {
        formattedPrice: {
            get() {
                return this.editedDeliveries && this.editedDeliveries.price !== undefined
                    ? Number(this.editedDeliveries.price).toFixed(2).replace(".", ",")
                    : "";
            },
            set(value) {
                let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
                this.editedDeliveries.price = isNaN(numericValue) ? 0.00 : numericValue;
            }
        }
    },
    created() {
        this.loadDeliveries();
    },
    methods: {
        async loadDeliveries() {
            this.loading = true;
            try {
                const response = await api.get("delivery/deliveries");
                if (response.data && Array.isArray(response.data)) {
                    this.deliveries = response.data.flat().map(delivery => ({
                        id: delivery.id,
                        recipient_name: delivery.recipient_name,
                        street: delivery.street,
                        number: delivery.number,
                        complement: delivery.complement,
                        city: delivery.city,
                        state: delivery.state,
                        zip_code: delivery.zip_code,
                        bairro: delivery.bairro,
                        country: delivery.country,
                        phone: delivery.phone,
                        price: delivery.total_value,
                        delivery_id: delivery.delivery_id
                     //   email: delivery.userEmail,

                    }));

                    console.log(response.data);
                } else {
                    console.error("Resposta não contém um array de entregas:", response.data);
                }
            } catch (error) {
                console.error("Erro ao carregar entregas:", error);
            } finally {
                this.loading = false;
            }
        },
        getCategoryName(categoryId) {
            // Implemente aqui a lógica para buscar o nome da categoria baseado no categoryId
            return "Categoria Exemplo"; // Exemplo de retorno
        },
        deleteProduct(productId) {
            // Lógica para excluir o produto
            console.log("Deletando produto:", productId);
        },
    }
};
</script>
