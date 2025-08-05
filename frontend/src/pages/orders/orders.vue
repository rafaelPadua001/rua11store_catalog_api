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


                <v-data-table :headers="headers" :items="orders" :items-per-page="10" class="elevation-1" item-key="id"
                    fixed-header height="500" :loading="loading" loading-text="Loading deliveries...">

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

                <v-dialog v-model="dialogCheckItems" max-width="800px">

                    <v-card>
                        <v-card-title>
                            <span class="headline">Detalhes do Pedido</span>
                        </v-card-title>


                        <v-card-subtitle>
                            <!-- {{ selectedOrderItems }} -->
                            <v-row v-for="(item, index) in selectedOrderItems" :key="index">
                                <v-col cols="auto" sm="12">
                                    <strong>Order</strong>
                                      <v-divider></v-divider>

                                </v-col>
                                <v-row>
                                      <v-col cols="auto" sm="4">
                                    <v-card width="120">
                                        <v-img 
                                            v-if="item.product_image"
                                            :src="item.product_image"
                                            :alt="item.seo?.slug || item.name"
                                            max-width="120"
                                            max-height="120"
                                            contain
                                            class="rounded-lg">
                                        </v-img>
                                    </v-card>
                                </v-col>
                                 <v-col cols="auto" sm="">
                                    <strong>OrderId:</strong> #{{ selectedOrder.id }}
                                    
                                </v-col>
                                <v-col cols="auto" sm="6">
                                     <strong>Product Name:</strong> {{ item.name }}
                                </v-col>
                                 <v-col cols="auto" sm="6">
                                    <strong>Unit Value:</strong> R$ {{ Number(item.unit_price).toFixed(2) }}
                                </v-col>
                                  
                                 <v-col cols="auto" sm="6">
                                    <strong>Total Value:</strong> R$ {{ Number(item.total_price).toFixed(2) }}
                                </v-col>

                                  <v-col cols="auto" sm="12">
                                    <strong>Description:</strong> {{ item.description }}
                                </v-col>
                                </v-row>
                            
                            </v-row>

                           <v-row>
                            <v-col cols="auto" sm="12">
                                <strong>Delivery</strong>
                                <v-divider></v-divider>
                            </v-col>
                              <v-col cols="auto" sm="6">
    <strong>ID:</strong> {{ selectedOrderDelivery.id }}
  </v-col>
                            <v-col cols="auto" sm="6">
    <strong>Melhor Envio ID:</strong> {{ selectedOrderDelivery.melhorenvio_id }}
  </v-col>
                            <v-col cols="auto" sm="6">
                                <strong>User id</strong> {{ selectedOrder.user_id }}
                            </v-col>
                              <v-col cols="auto" sm="6">
    <strong>Recipient Name:</strong> {{ selectedOrderDelivery.recipient_name }}
  </v-col>
    <v-col cols="auto" sm="6">
    <strong>Phone:</strong> {{ selectedOrderDelivery.phone }}
  </v-col>
   <v-col cols="auto" sm="6">
    <strong>Bairro:</strong>  {{ selectedOrderDelivery.bairro }}
  </v-col>
   <v-col cols="auto" sm="6">
    <strong>Cidade:</strong>  {{ selectedOrderDelivery.city }}
  </v-col>
   <v-col cols="auto" sm="6">
    <strong>Address:</strong>  {{ selectedOrderDelivery.street }} {{ selectedOrderDelivery.number }} {{ selectedOrderDelivery.complement }} {{ selectedOrderDelivery.bairro }}
  </v-col>
   <v-col cols="auto" sm="6">
    <strong>Complement:</strong> {{ selectedOrderDelivery.complement }}
  </v-col>
  <v-col cols="auto" sm="6">
    <strong>Preço:</strong> R$ {{ selectedOrderDelivery.total_value }}
  </v-col>
                            <v-col cols="auto" sm="6">
                                <strong>total_amount</strong> {{ selectedOrder.total_amount }}
                            </v-col>
                            <v-col cols="auto" sm="6">
                                <strong>zipcode:</strong> {{ selectedOrder.shipment_info }} 
                            </v-col>
                           <v-col cols="auto" sm="4">
                            <strong>Status</strong>
                            <v-chip v-if="selectedOrder.status === 'approved'" color="success">{{ selectedOrder.status }}</v-chip> 
                           </v-col>
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
        : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    data() {
        return {
            loading: false,
            orders: [],
            selectedOrderItems: [],
            selectedOrder: null,
            selectedOrderDelivery: null,
            headers: [
                { title: "ID", key: "id" },
                { title: "User ID", key: "user_id" },
                { title: "Payment ID", key: "payment_id" },
                { title: "Delivery ID", key: "delivery_id" },
                { title: "shipment info", key: "shipment_info" },
                { title: "Order date", key: "order_date" },
                { title: "status", key: "status" },
                { title: "Total amount", key: "total_amount" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
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

                // Garante que sempre será um array simples
                const ordersArray = Array.isArray(response.data) ? response.data.flat() : [];

                console.log("Orders recebidos:", ordersArray);

                this.orders = ordersArray.map(order => {
                    const items = (order.products || []).map((prod, index) => ({
                        ...prod,
                        seo: order.product_seo?.[index] || {},
                        delivery: order.product_delivery?.[index] || {}
                    }));

                    return {
                        id: order.id,
                        user_id: order.user_id,
                        payment_id: order.payment_id,
                        shipment_info: order.shipment_info,
                        order_date: order.order_date,
                        status: order.status,
                        total_amount: order.total_amount,
                        delivery_id: Array.isArray(order.delivery_id) ? order.delivery_id[0] : order.delivery_id,
                        delivery: order.delivery,
                        items
                    };
                });
            } catch (error) {
                console.error("Erro ao carregar pedidos:", error);
                this.orders = [];
            } finally {
                this.loading = false;
            }
        },
        async checkItemInCart(order) {
            this.selectedOrder = order;
            this.selectedOrderItems = order.items;
            this.selectedOrderDelivery = order.delivery;
            
            this.dialogCheckItems = true;
        },

    }
};
</script>
