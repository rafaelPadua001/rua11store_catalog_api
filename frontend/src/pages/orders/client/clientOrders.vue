<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-toolbar>
                    <v-toolbar-title>
                        <v-card-title>Orders</v-card-title>
                    </v-toolbar-title>
                </v-toolbar>

                <v-card-text v-if="!orders">
                    {{orders}}
                </v-card-text>
                <v-card-text v-else>
                    Não encontramos nenhum pedido para o seu usuário
                </v-card-text>
                
            </v-card>
        </v-col>
    </v-row>

</template>

<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';

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
    try{
        response = await api.get(`order/get-order/${userId}`)
         orders.value = response.data;
    }
    catch(e){
        alert('Erro ao buscar orders, tente novamente.', e);
    }
}

onMounted(() => {
    getOrders();
})
</script>