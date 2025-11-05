<template>
    <v-row justify="center">
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card>
                <v-toolbar color="transparent">
                    <v-toolbar-title>Coupons</v-toolbar-title>
                </v-toolbar>

                <v-divider></v-divider>

                <v-card-text>
                    <!-- ✅ Loading -->
                    <div v-if="loading" class="d-flex justify-center my-6">
                        <v-progress-circular indeterminate></v-progress-circular>
                    </div>

                    <!-- ✅ Nenhum cupom -->
                    <div v-else-if="coupons.length === 0" class="text-center py-8">
                        <v-icon size="60">mdi-ticket-off-outline</v-icon>
                        <p class="mt-2">Nenhum cupom disponível</p>
                    </div>


                    <v-row v-else v-for="(coupon, index) in coupons" :key="index" class="align-center">
                        <v-col cols="3">
                            <v-img :src="coupon.coupon.image_path" :alt="coupon.title" max-width="200"
                                max-height="100"></v-img>
                        </v-col>
                        <v-col cols="3">
                            <div>
                                <strong>{{ coupon.title }}</strong>
                            </div>
                            <div>
                                <strong>Code:</strong> {{ coupon.code }}
                                <v-btn variant="text" size="small" color="primary" class="ml-2"
                                    @click="copyCode(coupon.code)">
                                    Copy
                                </v-btn>
                            </div>
                        </v-col>
                        <v-col cols="3">
                            <div>
                                <strong>Initial date: </strong> {{ formatDate(coupon.start_date) }}
                            </div>
                            <div>
                                <strong>End date: </strong> {{ formatDate(coupon.end_date) }}
                            </div>
                        </v-col>
                        <v-col cols="3">
                            <div><strong>Discount:</strong> {{ coupon.discount }}%</div>
                            <v-btn color="red" @click="removeCoupon(coupon.id)" variant="text">
                                <v-icon size="x-large">mdi-delete</v-icon>
                            </v-btn>
                        </v-col>
                        <v-col cols="12">
                            <v-divider class="my-2"></v-divider>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
// import { useToast } from 'vue-toastification' 

const userId = localStorage.getItem('user_id');
const coupons = ref([]);
const loading = ref(false);
//  const toast = useToast?.();
const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const getCoupons = async () => {
    loading.value = true;
    try {
        const response = await api.get(`/coupon/get-coupons/${userId}`);
        if (response.status === 200 || response.status === 201) {
            coupons.value = response.data;
        }


    }
    catch (e) {
        console.log('Erro ao buscar cupons', e);
    }
    finally {
        loading.value = false;
    }
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { timeZone: 'UTC' });
}

const copyCode = async (code) => {
    try {
        await navigator.clipboard.writeText(code)
        alert('código copiado !')

    }
    catch (e) {
        //toast.error('Erro ao copiar código', e);
        alert('Falha ao copiar')

    }
};

const removeCoupon = async (couponId) => {
    try {
        const userId = localStorage.getItem('user_id')
        const response = await api.delete(`/coupon/delete-coupons-by-client/${couponId}`, {
            params: { userId }
        });
        return coupons.value = coupons.value.filter(c => c.id !== couponId);
    }
    catch (e) {
        alert('erro ao remover coupon', e);
    }
};

onMounted(() => {
    getCoupons();
})

</script>