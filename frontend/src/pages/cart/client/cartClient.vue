<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-toolbar>
                    <v-toolbar-title>
                        <v-card-title>
                            <v-icon>mdi-cart</v-icon>
                            Cart
                        </v-card-title>

                    </v-toolbar-title>
                </v-toolbar>


                <v-divider></v-divider>

                <v-card-text>
                    <div v-if="cartItens && cartItens.items && cartItens.items.length">
                        <div v-for="(item, index) in cartItens.items" :key="index">
                            <v-card elevation="0">
                                <v-row no-gutters align="center">
                                    <v-col cols="3">
                                        <v-img :src="item.product_image" height="150" contain></v-img>
                                    </v-col>
                                    <v-col cols="9">
                                        <div class="text-subtitle-2 font-weight-bold">{{ item.product_name }}</div>
                                        <div class="text-body-2"><strong>Price:</strong> R$ {{ item.product_price }}
                                        </div>
                                        <div class="text-caption"><strong>Qtd:</strong> {{ item.quantity }}
                                            <v-col cols="12" sm="12" md="4">
                                                <v-text-field v-model.number="item.quantity" type="number" min="1"
                                                    density="compact" hide-details style="width: 80px;" @click.stop
                                                    @mousedown.stop />
                                            </v-col>
                                        </div>
                                    </v-col>
                                </v-row>

                                <v-divider></v-divider>
                            </v-card>
                        </div>
                        <br></br>
                        <v-row justify="center" no-gutters>
                            <v-col cols="12" md="2">
                                <v-btn variant="tonal" color="success" @click="checkout(cartItens)" prepend-icon="mdi-credit-card">
                                    Pagar
                                </v-btn>
                            </v-col>
                        </v-row>
                    </div>

                    <div v-else>
                        <v-alert color="grey" variant="tonal" text>
                            Carrinho vazio.
                        </v-alert>
                    </div>
                </v-card-text>

            </v-card>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
import axios from 'axios'


const cartItens = ref([]);
const userId = localStorage.getItem('user_id');
const token = localStorage.getItem("access_token") || localStorage.getItem('token');
const router = useRouter();
const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const getItemsCart = async () => {
    try {
        const response = await api.get(`cart/get-cart/${userId}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        cartItens.value = response.data[0];
    }
    catch (e) {
        console.log('erro ao buscar itens:', e);
    }
}

const checkout = (item) => {
    router.push({path: '/payments/client/checkout', query: {item: JSON.stringify(item)}})
}

onMounted(() => {
    getItemsCart();
})

</script>