<template>
  <v-row justify="center" no-gutters>
    <v-col cols="12" sm="10" md="8" lg="6">
      <v-card class="pa-4" elevation="0">
        <v-toolbar color="transparent" flat>
          <v-toolbar-title class="text-h6 text-md-h5">Orders</v-toolbar-title>
        </v-toolbar>

        <v-divider :thickness="2" class="mb-4" />

        <v-card-text v-if="orders && orders.length">
          <div v-for="(order, index) in orders" :key="index" class="mb-4">
            <v-card class="pa-2" elevation="1">
              <!-- Cabeçalho do pedido -->
              <v-card-title class="py-2">
                <v-row class="align-center">
                  <v-col cols="12" sm="6">
                    <strong>Order #{{ order.id }}</strong>
                  </v-col>

                  <v-col cols="12" sm="6" class="text-sm-end">
                    <strong>Status:</strong>
                    <v-chip
                      v-if="order.status === 'pending'"
                      color="warning"
                      size="small"
                      class="text-uppercase"
                    >
                      {{ order.status }}
                    </v-chip>

                    <v-chip
                      v-else-if="order.status === 'rejected' || order.status === '400' || order.status === '401'"
                      color="error"
                      size="small"
                      class="text-uppercase"
                    >
                      {{ order.status }}
                    </v-chip>

                    <v-chip
                      v-else
                      color="success"
                      size="small"
                      class="text-uppercase"
                    >
                      {{ order.status }}
                    </v-chip>
                  </v-col>
                </v-row>
              </v-card-title>

              <v-divider />

              <!-- Produtos -->
              <v-card-text>
                <v-row
                  v-for="(product, i) in order.products"
                  :key="i"
                  class="py-3"
                  align="center"
                >
                  <v-col cols="12" sm="3" class="text-center">
                    <v-img
                      :src="product.product_image"
                      :alt="product.product_name"
                      max-width="90"
                      class="mx-auto rounded-lg"
                      contain
                    />
                  </v-col>

                  <v-col cols="12" sm="9">
                    <div class="text-subtitle-1 font-weight-medium mb-1">
                      {{ product.name }}
                    </div>

                    <div class="text-body-2">
                      <strong>Category:</strong>
                      <v-chip
                        v-for="(category, ci) in order.categories"
                        :key="ci"
                        color="primary"
                        size="x-small"
                        class="ma-1"
                      >
                        {{ category.name }}
                      </v-chip>
                    </div>

                    <div class="text-body-2 mt-2">
                      <strong>Qtd:</strong> {{ product.quantity }} |
                      <strong>Price:</strong> R${{ product.unit_price }}
                    </div>

                    <div class="text-body-2 mt-1">
                      <strong>Total:</strong> R${{ order.total_amount }}
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>

              <v-divider />

              <v-card-actions class="justify-end">
                <v-btn
                  variant="tonal"
                  color="success"
                  size="small"
                  @click="checkout(order)"
                >
                  Repetir o pedido
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </v-card-text>

        <v-card-text v-else>
          <v-alert type="info" variant="tonal">
            Não encontramos nenhum pedido para o seu usuário.
          </v-alert>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const userId = localStorage.getItem('user_id');
const orders = ref([]);

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const getOrders = async () => {
    try {
        const response = await api.get(`/order/get-order/${userId}`)
        orders.value = response.data;
        console.log(response);
    }
    catch (e) {
        console.log('Erro ao buscar orders, tente novamente.', e);
    }
};
const checkout = async (item) => {
    router.push({path: '/payments/client/checkout', query: {item: JSON.stringify(item)}})
};
onMounted(() => {
    getOrders();
})
</script>