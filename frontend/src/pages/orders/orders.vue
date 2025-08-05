<template>
  <v-row justify="center" no-gutters>
    <v-col cols="12" sm="12" md="10" lg="10" xl="6">
      <v-card class="pa-4" elevation="0">
        <v-card-title class="d-flex justify-center">
          <h5>Orders Management</h5>
        </v-card-title>
        <v-divider></v-divider>

        <!-- Botão adicionar produto (desativado) -->
        <!-- 
        <v-card-actions class="d-flex justify-end mb-4">
          <v-btn color="primary" @click="newProduct" disabled>
            <v-icon left>mdi-plus</v-icon>
            Add Product
          </v-btn>
        </v-card-actions> 
        -->

        <v-data-table
          :headers="headers"
          :items="orders"
          :items-per-page="10"
          class="elevation-1"
          item-key="id"
          fixed-header
          height="500"
          :loading="loading"
          loading-text="Loading deliveries..."
        >
          <!-- Exibe a descrição do produto -->
          <template v-slot:item.description="{ item }">
            <span>
              {{ item.description?.length > 38 ? item.description.substring(0, 38) + '...' : item.description }}
            </span>
          </template>

          <!-- Ações -->
          <template v-slot:item.actions="{ item }">
            <!-- Botão buscar item no carrinho -->
            <v-icon small @click.stop="checkItemInCart(item)">
              mdi-file-search
            </v-icon>

            <!-- Ícone deletar produto -->
            <v-icon small @click.stop="deleteItemCart(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>

        <!-- Diálogo -->
        <v-dialog v-model="dialogCheckItems" max-width="900" fullscreen="$vuetify.display.smAndDown">
          <v-card class="pa-4">
            <v-toolbar flat>
              <v-toolbar-title class="headline">Detalhes do Pedido</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon @click="dialogCheckItems = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-toolbar>

            <!-- Order -->
            <v-row>
              <v-col cols="12">
                <strong>Order</strong>
                <v-divider></v-divider>
              </v-col>

              <v-col cols="12" sm="2">
                <v-card width="120">
                  <v-img
                    v-if="selectedOrderItems[0]?.product_image"
                    :src="selectedOrderItems[0].product_image"
                    :alt="selectedOrderItems[0].seo?.slug || selectedOrderItems[0]?.name"
                    max-width="120"
                    max-height="120"
                    contain
                    class="rounded-lg"
                  />
                </v-card>
              </v-col>

             <!-- <v-col cols="12" sm="2">
                <strong>OrderId:</strong> #{{ selectedOrder.id }}
              </v-col> -->
              <v-col cols="12" sm="3">
                <strong>Product Name:</strong> {{ selectedOrderItems[0]?.name }}
              </v-col>
              <v-col cols="12" sm="3">
                <strong>Unit Value:</strong> R$ {{ Number(selectedOrderItems[0]?.unit_price).toFixed(2) }}
              </v-col>
              <v-col cols="12" sm="2">
                <strong>Total Value:</strong> R$ {{ Number(selectedOrderItems[0]?.total_price).toFixed(2) }}
              </v-col>
            <!--  <v-col cols="12">
                <strong>Description:</strong> {{ selectedOrderItems[0]?.description }}
              </v-col> -->
            </v-row>

            <!-- Delivery -->
            <v-row class="mt-4">
              <v-col cols="12">
                <strong>Delivery</strong>
                <v-divider></v-divider>
              </v-col>

              <v-col cols="12" sm="6">
                <strong>ID:</strong> {{ selectedOrderDelivery?.id }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>Melhor Envio ID:</strong> {{ selectedOrderDelivery?.melhorenvio_id }}
              </v-col>
              <v-col cols="12" sm="8">
                <strong>User id:</strong> {{ selectedOrder.user_id }}
              </v-col>
              <v-col cols="12" sm="4">
                <strong>Recipient Name:</strong> {{ selectedOrderDelivery?.recipient_name }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>Phone:</strong> {{ selectedOrderDelivery?.phone }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>Bairro:</strong> {{ selectedOrderDelivery?.bairro }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>Cidade:</strong> {{ selectedOrderDelivery?.city }}
              </v-col>
              <v-col cols="12">
                <strong>Address:</strong>
                {{ selectedOrderDelivery?.street }} {{ selectedOrderDelivery?.number }} {{ selectedOrderDelivery?.complement }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>Complement:</strong> {{ selectedOrderDelivery?.complement }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>zipcode:</strong> {{ selectedOrder.shipment_info }}
              </v-col>
              <v-col cols="12" sm="3">
                <strong>Preço:</strong> R$ {{ selectedOrderDelivery?.total_value }}
              </v-col>
              <v-col cols="12" sm="3">
                <strong>total_amount:</strong> {{ selectedOrder.total_amount }}
              </v-col>
              <v-col cols="12" sm="6">
                <strong>Status:</strong>
                <v-chip v-if="selectedOrder.status === 'approved'" color="success">
                  {{ selectedOrder.status }}
                </v-chip>
              </v-col>
            </v-row>

            <!-- Dados de entrega do carrinho (comentado) -->
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
            </v-card-subtitle>
            -->

            <v-card-actions>
              <!-- Botão compra etiqueta no carrinho -->
              <!-- 
              <v-btn small @click.stop="shipmentCheckout(cartItems.data)">
                checkout
              </v-btn> 
              -->
              <v-spacer></v-spacer>
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
