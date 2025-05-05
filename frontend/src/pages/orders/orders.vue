<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="10" xl="10" sm="12">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Orders Management</h1>
                </v-card-title>

                <!-- <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct" disabled>
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions> -->

                <v-data-table :headers="headers" :items="orders" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading deliveries...">
                    <!-- Exibe imagens de produtos -->
                    <!-- <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template> -->

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
                   

                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                      

                         <!-- Botão de buscar item no carrinho  -->
                        <v-icon small @click.stop="checkItemInCart(item)">
                            mdi-file-search
                        </v-icon>

                      
                         <!-- Ícone de deletar produto  -->
                        <v-icon small @click.stop="deleteItemCart(item)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>

                <v-dialog v-model="dialogCheckItems" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">Detalhes do Produto</span>
                        </v-card-title>
                        

                        <v-card-subtitle>
                            <!-- {{ selectedOrderItems }} -->
                            <v-row v-for="(item, index) in selectedOrderItems" :key="index" class="mb-4">
                                <v-col cols="12" sm="6">
                                    <strong>Nome do Produto:</strong> {{ item.product_name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Descrição:</strong> {{ item.product_description }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Quantidade:</strong> {{ item.quantity }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Preço Unitário:</strong> R$ {{ item.unit_price.toFixed(2) }}
                                </v-col>
                                <!-- <v-col cols="12" sm="6">
                                    <strong>Preço Total:</strong> R$ {{ item.total_price.toFixed(2) }}
                                </v-col> -->
                            </v-row>

                        </v-card-subtitle>
                        
<!-- 
                        <v-card-subtitle>
                            <v-row>
                                <v-col cols="12" sm="6">
                                    <strong>Nome do Destinatário:</strong> {{ cartItems.data.to.name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Endereço:</strong> {{ cartItems.data.to.address }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Cidade:</strong> {{ cartItems.data.to.city }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Estado:</strong> {{ cartItems.data.to.state }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Telefone:</strong> {{ cartItems.data.to.phone }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Email:</strong> {{ cartItems.data.to.email }}
                                </v-col>
                            </v-row>
                        </v-card-subtitle> -->

                        <v-card-actions>
                             <!-- Botão de compra de etiqueta no carrinho  -->
                              <!-- <v-btn small @click.stop="shipmentCheckout(cartItems.data)">
                                checkout
                              </v-btn> -->
                            
                            <v-btn color="green" text @click="dialogCheckItems = false">Close</v-btn>
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
    data() {
        return {
            loading: false,
            orders: [],
            selectedOrderItems: [],
            headers: [
                { text: "ID", value: "id" },
                { text: "User ID", value: "user_id" },
                { text: "Payment ID", value: "payment_id" },
                { text: "shipment info", value: "shipment_info" },
                { text: "Order date", value: "order_date" },
                { text: "status", value: "status" },
                { text: "Total amount", value: "total_amount" },
                { text: "Actions", value: "actions", width: "120px", align: "center", sortable: false },
            ],
            isPaymentButtonPayTagDisabled: true,
            dialogCheckItems: false,
        };
    },
    // computed: {
    //     formattedPrice: {
    //         get() {
    //             return this.editedDeliveries && this.editedDeliveries.price !== undefined
    //                 ? Number(this.editedDeliveries.price).toFixed(2).replace(".", ",")
    //                 : "";
    //         },
    //         set(value) {
    //             let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
    //             this.editedDeliveries.price = isNaN(numericValue) ? 0.00 : numericValue;
    //         }
    //     }
    // },
    created() {
        this.loadOrders();
    },
    methods: {
        async loadOrders() {
            this.loading = true;
            try {
                const response = await api.get("order/get-orders");
                if (response.data && Array.isArray(response.data)) {
                    this.orders = response.data.flat().map(order => ({
                        id: order.id,
                        user_id: order.user_id,
                        payment_id: order.payment_id,
                        shipment_info: order.shipment_info,
                        order_date: order.order_date,
                        status: order.status,
                        total_amount: order.total_amount,
                        items: order.items

                    }));

                    // console.log(response.data);
                } else {
                    console.error("Resposta não contém um array de entregas:", response.data);
                }
            } catch (error) {
                console.error("Erro ao carregar entregas:", error);
            } finally {
                this.loading = false;
            }
        },
        async checkItemInCart(item) {
          this.selectedOrderItems = item.items;
          this.dialogCheckItems = true
        },
     
    }
};
</script>
