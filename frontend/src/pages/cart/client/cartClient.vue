<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">

                <v-toolbar flat>
                    <v-row class="w-100" no-gutters>
                        <!-- Esquerda -->
                        <v-col>
                            <div class="d-flex align-center">
                                <v-icon class="mr-2">mdi-cart</v-icon>
                                <span class="font-weight-medium">
                                    Carrinho ({{ cartItens?.items?.length || 0 }})
                                </span>
                            </div>
                        </v-col>

                        <!-- Direita -->
                        <v-col class="text-right">
                            <div class="text-subtitle-2 font-weight-bold">
                                Total: R$
                                {{ totalValue.toLocaleString("pt-BR", { minimumFractionDigits: 2 }) }}
                            </div>
                        </v-col>
                    </v-row>
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
                                    <v-col cols="6">
                                        <div class="text-subtitle-2 font-weight-bold">{{ item.product_name }}</div>
                                        <div class="text-body-2"><strong>Price:</strong> R$ {{ item.product_price }}
                                        </div>
                                        <div class="text-caption">
                                            <strong>Qtd:</strong>
                                            {{ item.quantity }}
                                            <v-col cols="8" sm="8" md="4">
                                                <v-text-field v-model.number="item.quantity" type="number" min="1"
                                                    density="compact" hide-details style="width: 80px;" @click.stop
                                                    @mousedown.stop variant="underlined" />
                                            </v-col>
                                        </div>
                                    </v-col>
                                    <v-col cols="3">
                                        <v-btn color="error" variant="text" @click="removeItem(item)">
                                            <v-icon>mdi-delete</v-icon>
                                        </v-btn>
                                    </v-col>

                                </v-row>

                                <v-divider></v-divider>
                            </v-card>
                        </div>
                        <br></br>
                        <v-row justify="center" no-gutters>
                            <v-col cols="12" md="2">
                                <v-btn variant="tonal" color="success" @click="checkout(cartItens)"
                                    prepend-icon="mdi-credit-card">
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


const cartItens = ref({ items: [] });

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
};

const totalValue = computed(() => {
    const items = cartItens?.value.items;

    if (!items) return 0;

    return items.reduce((sum, item) => {
        return sum + Number(item.product_price) * Number(item.quantity);
    }, 0);
});

const checkout = (item) => {
    sessionStorage.setItem('checkout_item', JSON.stringify(item));
    router.push('/payments/client/checkout');
};

const removeItem = async (item) => {
    if (!confirm(`Tem certeza que deseja remover ${item.product_name}`)) return;
    try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        const response = await api.delete(`cart/cart-item-remove/${item.id}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            }
        });

        if (cartItens.value && Array.isArray(cartItens.value.items)) {
            return cartItens.value.items = cartItens.value.items.filter(i => i.id !== item.id);
        }
        else if (Array.isArray(cartItens.value)) {
            cartItens.value = cartItens.value.filter(i => i.id !== item.id)
        }

    }
    catch (e) {
        alert('Não foi possível remover item. Tente novamente', e);
    }
};

onMounted(() => {
    getItemsCart();
})

</script>