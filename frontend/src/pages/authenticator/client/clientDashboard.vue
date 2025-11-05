<template>
    <v-container class="py-6">
        <v-row justify="center" dense>
            <v-col cols="auto" class="d-flex flex-column">
                <div>
                    <v-chip @click="goToCart" class="cursor-pointer">
                        <v-icon>mdi-cart-plus</v-icon>
                        Cart items: ({{ carts[0]?.items?.length || 0 }})
                    </v-chip>

                    <v-chip @click="goToOrders" class="cursor-pointer">
                        <v-icon>mdi-shopping</v-icon>
                        Orders ({{ orders[0]?.length || 0 }})
                    </v-chip>
                    <v-chip @click="goToCoupons" class="cursor-pointer">
                        <v-icon>mdi-ticket</v-icon>
                        Coupons ({{ coupons[0]?.length || 0 }})
                    </v-chip>
                </div>
            </v-col>
        </v-row>
        <br></br>
        <v-divider></v-divider>

        <v-row dense>
            <v-col cols="auto">
                <p class="text-h6">Pedidos por Categoria:</p>
            </v-col>
        </v-row>

        <v-row>
            <v-col v-if="orders[0]?.length >= 1">
                Graph here
            </v-col>
            <v-col>
                <v-card height="300">
                    <canvas ref="chartCanvas"></canvas>
                </v-card>
            </v-col>

        </v-row>

        <v-row>
            <v-col class="d-flex flex-column">
                <v-card>
                    <v-row>
                        <v-col>
                            <p class="text-h6">Last Actives:</p>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col v-if="orders[0]?.length >= 1">
                            Last activies Here...
                        </v-col>
                        <v-col v-else>
                            <v-card>
                                <v-card-text>
                                    Nenhum pedido encontrado
                                </v-card-text>
                            </v-card>

                        </v-col>
                    </v-row>

                </v-card>
            </v-col>

        </v-row>


    </v-container>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
import { Chart, registerables } from 'chart.js';

const router = useRouter();
const userId = localStorage.getItem('user_id');
const token = localStorage.getItem('access_token') || localStorage.getItem('token');
const carts = ref([]);
const orders = ref([]);
const coupons = ref([]);
const chartCanvas = ref(null);
let chartInstance = null;



const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

Chart.register(...registerables)

const getCartsByUserId = async () => {
    try {
        const response = await api.get(`/cart/get-cart/${userId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.status === 200 || response.status === 201) {
            carts.value = response.data;
        }
        else {
            console.log('nenhum carrinho associado a este usuario.');
        }

    }
    catch (e) {
        console.log('Erro ao receber carrrinho, tente novamente', e);
    }
};

const getOrdersByUserId = async () => {
    try {
        const response = await api.get(`/order/get-order/${userId}`)
        if (response.status === 200 || response.status === 201) {
            orders.value = response.data;
        }
        else {
            if (response.status === 404) {
                console.log('nenhuma pedido encontrado...');
                orders.value = [];
            }
            console.log('nenhuma order associada ao usuário foi encontrado');
        }
    }
    catch (e) {
        console.log('Erro ao buscar orders.', e);
    }
};

const getCouponsByUserId = async () => {
    try {
        const response = await api.get(`/coupon/get-coupons/${userId}`);
        if (response.status === 200 || response.status === 201) {
            coupons.value = response.data;
        }
        else {
            console.log('nenhuma coupon encontrado.');
        }
    }
    catch (e) {
        console.log('Nenhum coupon associado ao usuário foi encontrado.', e);
    }
};

const goToCart = () => {
    router.push('/cart/client/cartClient');
};

const goToOrders = () => {
    router.push('/orders/client/clientOrders');
};

const goToCoupons = () => {
    router.push('/coupons/client/clientCoupons');
};

const createChart = (data) => {
    if (chartInstance) chartInstance.destroy()

    chartInstance = new Chart(chartCanvas.value, {
        type: "pie",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Orders",
                    data: data.values,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
};

const refreshChart = () => {
    if (!orders.value || orders.value.length === 0) {
        createChart({
            labels: ["Nenhum pedido realizado"],
            values: [1]
        })
    }
    else {
        createChart({
            labels: orders.value.map(o => o.name),
            values: orders.value.map(o => o.total)
        })
    }
};

onMounted(refreshChart)
watch(() => orders, refreshChart)


onMounted(() => {
    getCartsByUserId();
    getOrdersByUserId();
    getCouponsByUserId();
})


</script>
