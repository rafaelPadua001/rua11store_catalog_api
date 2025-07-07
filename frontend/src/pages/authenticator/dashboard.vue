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
                    <v-card-title>Carrinhos Ativos</v-card-title>
                    <v-card-text class="text-h5 font-weight-bold">{{ carts?.length || 0 }}</v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" sm="4">
                <v-card class="pa-4">
                    <v-card-title>Pedidos de Hoje</v-card-title>

                    <v-card-text class="text-h5 font-weight-bold">{{ orders?.length || 0 }}</v-card-text>
                </v-card>
            </v-col>


             <v-col cols="12" sm="4">
        <v-card class="pa-3">
          <v-card-title>Receita Total</v-card-title>
          <v-card-text class="text-h5 font-weight-bold">
            R$ {{ totalRevenue.toFixed(2) }}
          </v-card-text>
        </v-card>
      </v-col>
  

        </v-row>

        <v-row>
            <v-col cols="12" sm="4">
                <v-card>
                    <v-card-title>Produtos Mais Pedidos</v-card-title>
                    <v-card-title class="text-h5 font-weight-bold">Mais pedidos aqui...</v-card-title>
                </v-card>
            </v-col>
            <v-col cols="12" sm="4">
                <v-card>
                    <v-card-title>Fora do Estoque</v-card-title>
                    <v-card-title class="text-h5 font-weight-bold">Produtos fora do estoque aqui...</v-card-title>
                </v-card>
            </v-col>
        </v-row>



        <!-- Seção futura para grafico ou tabela -->
        <v-row>
            <v-col cols="12">
                <v-card class="pa-4">
                    <v-card-title>Vendas nos ultimos 7 dias</v-card-title>
                    <v-card-text>
                        <p>Gráfico de exemplo...</p>
                    </v-card-text>
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


export default {
    data() {
        return {
            profile: null,
            carts: null,
            orders: [],
            ordersAll: [],
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
    console.log(`Pedido ID ${order.id}: ${raw} -> ${val}`);
    return isNaN(val) ? 0 : val;
  });

  const total = valores.reduce((sum, val) => sum + val, 0);
  console.log("💰 Soma final:", total);
  return total;
}

  },
   

    methods: {
        capitalizeFirstLetter(text) {
            return text.charAt(0).toUpperCase() + text.slice(1);
        },
        async waitForToken(retries = 10, delay = 300) {
            for (let i = 0; i < retries; i++) {
                const token = localStorage.getItem('user_token');
                if (token) return token;
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
                    .from('cart')
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

        console.log('Todos os pedidos:', this.ordersAll);
        console.log('Pedidos de hoje:', this.ordersToday);
      } catch (error) {
        console.log('Erro ao buscar pedidos:', error);
      }
    }
  },
    mounted() {

        this.getProfileUser();
        this.loadorders();
        this.loadCarts();

    },

};
</script>