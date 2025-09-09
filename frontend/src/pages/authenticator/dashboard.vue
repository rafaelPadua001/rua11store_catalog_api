<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12">
                <v-card class="pa-4 mb-4">
                    <v-row align="center">
                        <v-col cols="auto">
                            <v-icon color="primary" size="36">
                                <v-avatar size="48">
                                    <v-img
                                        src="https://imgs.search.brave.com/Zsapxs7JqY0v8BYpGwgMnI1WLK_J9l-O1IMIOUuzTGc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9waWNz/LmNyYWl5b24uY29t/LzIwMjQtMDktMDcv/djc1XzNnV0VUTWVL/UHJmWmFXWlFKQS53/ZWJw" />
                                </v-avatar></v-icon>
                        </v-col>
                        <v-col>
                            <div class="text-h5 font-weight-bold" v-if="profile">Bem-vindo de volta,
                                Sr.{{ profile.full_name }}</div>
                            <div class="text-subtitle-2">{{ dateToday }}</div>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>

        <!-- Cads Resumo-->
        <v-row>
            <v-col cols="12" sm="4">
                <v-card class="pa-4">
                    <v-card-title>🛒 Carrinhos Ativos</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="text-h5 font-weight-bold">{{ carts?.length || 0 }}</v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" sm="4">
                <v-card class="pa-4">
                    <v-card-title>📦 Pedidos de Hoje</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="text-h5 font-weight-bold">{{ orders?.length || 0 }}</v-card-text>
                </v-card>
            </v-col>


            <v-col cols="12" sm="4">
                <v-card class="pa-3">
                    <v-card-title>💰 Receita Total</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="text-h5 font-weight-bold">
                        R$ {{ totalRevenue.toFixed(2) }}
                    </v-card-text>
                </v-card>
            </v-col>


        </v-row>

        <v-row>
            <v-col cols="12" sm="4"></v-col>
            <v-col cols="12" sm="4">
                <v-card>
                    <v-card-title>🔥 Produtos Mais Pedidos</v-card-title>
                    <v-divider></v-divider>
                    <div v-if="top5Products.length == 0">
                        <v-card-text>Nenhum produto encontrado</v-card-text>
                    </div>
                    <v-card-text>
                        <v-list dense>
                            <v-list-item v-for="(product, index) in top5Products" :key="product.id || index">
                                <div>
                                    <strong>{{ index + 1 }}. {{ product.name }}</strong><br>
                                    Quantidade: {{ product.totalQuantity }}
                                </div>
                            </v-list-item>
                        </v-list>
                    </v-card-text>

                </v-card>
            </v-col>
            <v-col cols="12" sm="4">
                <v-card>
                    <v-card-title>📦 Fora do Estoque</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <div v-if="stocks.length === 0">Todos os produtos estão em estoque !</div>
                        <v-list v-else>
                            <div v-for="(product, index) in stocks" :key="index" class="d-flex align-center mb-2">
                                <!-- Avatar -->
                                <v-avatar class="me-4" size="69">
                                    <v-img :src="product.product.thumbnail_path"
                                        :alt="product.product.seo?.slug || 'Produto'" cover />
                                </v-avatar>

                                <!-- Texto ao lado -->
                                <div class="text-truncate" style="max-width: 200px;">
                                    {{ product.product.name }}
                                </div>
                            </div>
                        </v-list>


                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>



        <!-- Seção futura para grafico ou tabela -->
        <v-row>
            <v-col cols="12">
                <v-card class="pa-4">
                    <v-card-title>📊 Vendas nos últimos 7 dias</v-card-title>

                    <!-- <v-card-subtitle class="text-subtitle-1">
                        Receita Total: <strong>R$ {{ revenueLast7Days.toFixed(2) }}</strong>
                    </v-card-subtitle>-->

                    <v-data-table :headers="ordersHeaders" :items="ordersLast7Days" class="elevation-1 mt-4"
                        item-value="id" dense>
                        <template #item.order_date="{ item }">
                            {{ new Date(item.order_date).toLocaleString('pt-BR') }}
                        </template>

                        <template #item.total_amount="{ item }">
                            R$ {{ parseFloat(item.total_amount).toFixed(2) }}
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
import { supabase } from '@/supabase';

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

function isValidJWT(token) {
  if (!token) return false;
  const parts = token.split('.');
  return parts.length === 3;
}

export default {
    data() {
        return {
            profile: null,
            carts: null,
            orders: [],
            ordersAll: [],
            ordersLast7Days: [],
            stocks: [],
            topProducts: [],
            top5Products: [],
            ordersHeaders: [
                { title: 'ID', key: 'id' },
                { title: 'Client', key: 'user_id' }, // ou ajuste conforme seu campo
                { title: 'Value', key: 'total_amount' },
                { title: 'Date', key: 'order_date' },
            ],
            dateToday: this.capitalizeFirstLetter(
                new Date().toLocaleDateString('pt-BR', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                })
            ),
        };
    },
    computed: {
        totalRevenue() {
            if (!Array.isArray(this.ordersAll) || this.ordersAll.length === 0) return 0;

            const valores = this.ordersAll.map(order => {
                const raw = order.total_amount;
                const val = parseFloat(raw);
                //.log(`Pedido ID ${order.id}: ${raw} -> ${val}`);
                return isNaN(val) ? 0 : val;
            });

            const total = valores.reduce((sum, val) => sum + val, 0);
            // console.log("💰 Soma final:", total);
            return total;
        },
        revenueLast7Days() {
            if (!Array.isArray(this.ordersLast7Days)) return 0;
            return this.ordersLast7Days.reduce((total, order) => {
                const value = parseFloat(order.total_amount);
                return total + (isNaN(value) ? 0 : value);
            }, 0);
        }
    },
    methods: {
        capitalizeFirstLetter(text) {
            return text.charAt(0).toUpperCase() + text.slice(1);
        },
        async waitForToken(retries = 10, delay = 300) {
            for (let i = 0; i < retries; i++) {
                const token = localStorage.getItem('access_token');
                if (token && isValidJWT(token)) return token;
                await new Promise(resolve => setTimeout(resolve, delay));
            }
            return null; // Se não encontrou o token após as tentativas
        },
        
        async getProfileUser() {
            try {
                const token = await this.waitForToken();
                // Verificando o token armazenado

                if (!token) {
                    console.error('Nenhum token encontrado. Faça login novamente.');
                    return;
                }
                const response = await api.get('/auth/profile', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },

                });

                this.profile = response.data;
            }
            catch (error) {
                console.log('Erro ao buscar perfil do usuario:', error);
            }
        },
        async loadCarts() {
            try {
                const { data, error } = await supabase
                    .from('carts')
                    .select('*')

                if (error) throw error
                this.carts = data;

            }
            catch (error) {
                console.log('Erro ao carregar carrinhos:', error);
            }
        },
        async loadorders() {
            try {
                const response = await api.get('/order/get-orders');
                const orders = Array.isArray(response.data) && Array.isArray(response.data[0])
                    ? response.data[0]
                    : response.data;

                this.ordersAll = orders;

                const today = new Date();
                today.setHours(0, 0, 0, 0);

                this.ordersToday = orders.filter(order => {
                    const orderDate = new Date(order.order_date);
                    orderDate.setHours(0, 0, 0, 0);
                    return orderDate.getTime() === today.getTime();
                });

                //Last 7d days orders
                const sevenDaysAgo = new Date();
                sevenDaysAgo.setDate(today.getDate() - 6); // today included
                sevenDaysAgo.setHours(0, 0, 0, 0);

                this.ordersLast7Days = orders.filter(order => {
                    const orderDate = new Date(order.order_date);
                    orderDate.setHours(0, 0, 0, 0);
                    return orderDate >= sevenDaysAgo && orderDate <= today;
                });

                //Most purchased products
                const productCountMap = {};

                orders.forEach(order => {
                    if (Array.isArray(order.products)) {
                        order.products.forEach(product => {
                            const key = product.id || product.name;
                            if (!productCountMap[key]) {
                                productCountMap[key] = {
                                    ...product,
                                    totalQuantity: 0
                                };
                            }

                            productCountMap[key].totalQuantity += product.quantity || 1;
                        });
                    }
                });

                //convert to array and sort
                this.topProducts = Object.values(productCountMap)
                    .sort((a, b) => b.totalQuantity - a.totalQuantity);

                // top 5 most sold
                this.top5Products = this.topProducts.slice(0, 5);
                //console.log('Pedidos de hoje:', this.ordersToday);
                //console.log('Todos os pedidos:', this.ordersAll);
                //console.log('Pedidos dos últimos 7 dias:', this.ordersLast7Days);
            } catch (error) {
                console.log('Erro ao buscar pedidos:', error);
            }
        },
        async loadStock() {
            try {
                const response = await api.get('/stock');
                this.stocks = response.data.filter(product => product.product_quantity === 0 && product.product);
                //  console.log('stock carregado:' , this.stocks);
            } catch (error) {
                console.log('Erro ao buscar estoque:', error);
            }
        }
    },
    mounted() {
        this.getProfileUser();
        this.loadorders();
        this.loadCarts();
        this.loadStock();
    },
};
</script>