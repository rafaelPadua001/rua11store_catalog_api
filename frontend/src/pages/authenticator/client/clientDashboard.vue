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
                        Orders ({{ orders.length || 0 }})
                    </v-chip>
                    <v-chip @click="goToCoupons" class="cursor-pointer">
                        <v-icon>mdi-ticket</v-icon>
                        Coupons ({{ coupons.length || 0 }})
                    </v-chip>
                </div>
            </v-col>
        </v-row>
        <br></br>


        <v-row>
            <v-col>
                <v-card height="300" elevation="0">
                    <canvas v-show="!loading" ref="chartCanvas"></canvas>

                    <div v-if="loading" class="d-flex justify-center align-center" style="height:100%">
                        <v-progress-circular indeterminate />
                    </div>
                </v-card>
            </v-col>
        </v-row>


        <v-row>
            <v-col class="d-flex flex-column">
                <v-card elevation="0">
                    <v-row>
                        <v-col>
                            <p class="text-h6">Last activies:</p>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row>
                        <v-col cols="12" class="d-flex flex-column justify-center" v-if="orders?.length >= 1">
                            <v-card v-for="(order, index) in orders" :key="index">
                                <v-card-text>
                                    <v-row>
                                        <v-col cols="11" class="d-flex flex-column">
                                            <p class="text-h6">Order {{ '#' + order.id }}</p>
                                        </v-col>
                                        <v-col>
                                            <span><strong>R$ {{ order.total_amount }}</strong></span>
                                        </v-col>
                                    </v-row>
                                    <v-row dense>
                                        <v-col md='11'>
                                            <span>Data: {{ formatDate(order.order_date) }}</span>
                                        </v-col>
                                        <v-col cols="auto" md="1">
                                            <v-chip v-if="order.status === 'pending' || order.status === 'in_process'"
                                                color="grey">
                                                {{ order.status }}
                                            </v-chip>
                                            <v-chip v-else-if="order.status === 'approved'" color="success">
                                                {{ order.status }}
                                            </v-chip>
                                            <v-chip v-else color="error">
                                                {{ order.status }}
                                            </v-chip>
                                        </v-col>
                                    </v-row>

                                </v-card-text>
                            </v-card>
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
import { useDate } from 'vuetify';

const router = useRouter();
const date = useDate()
const userId = ref(null);
const token = localStorage.getItem('access_token') || localStorage.getItem('token');
const carts = ref([]);
const orders = ref([]);
const coupons = ref([]);
const chartCanvas = ref(null);
let chartInstance = null;
const loading = ref(true)

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
        userId.value = localStorage.getItem('user_id');
        const response = await api.get(`/cart/get-cart/${userId.value}`, {
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
        userId.value = localStorage.getItem('user_id');
        const response = await api.get(`/order/get-order/${userId.value}`)

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
        userId.value = localStorage.getItem('user_id');
        const response = await api.get(`/coupon/get-coupons/${userId.value}`);
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
    if (!chartCanvas.value) return;
    if (!data?.labels?.length) return;

    if (chartInstance) chartInstance.destroy();
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
        //grouped orders
        const grouped = {};

        orders.value.forEach(o => {
            const cat = o.categories?.[0]?.name ?? "Sem Categoria";
            const total = o.total_amount ?? 0;

            if (!grouped[cat]) grouped[cat] = 0
            grouped[cat] += total
        });

        createChart({
            labels: Object.keys(grouped),
            values: Object.values(grouped)
        })
    }
};

const formatDate = (value) => {
    if (!value) return '';
    return date.format(value, 'keyboardDateTime');
}

onMounted(async () => {
    userId.value = localStorage.getItem('user_id');
    console.log(userId);
    if(!userId.value){
        console.warn("No user_id found, redirecting to login");
        //return router.push("/authenticator/login");
    }

    await Promise.all([
        getCartsByUserId(),
        getOrdersByUserId(),
        getCouponsByUserId()
    ]);
    loading.value = false;
    refreshChart();
});

watch(orders, () => {
    if (!loading.value) refreshChart()
})


</script>
