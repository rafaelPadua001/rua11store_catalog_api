<template>
    <v-row justify="center">
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card>
                <v-toolbar color="transparent">
                    <v-toolbar-title>You'r coupons</v-toolbar-title>
                </v-toolbar>

                <v-divider></v-divider>
                
                <v-card-text>
                    <v-row v-for="(coupon, index) in coupons">
                        <v-col cols="12">
                            {{ coupon.title }}
                        </v-col>
                        <v-col cols="12" sm="6">
                            <strong>Code:</strong> {{coupon.code}}
                            <v-btn variant="text" size="small" color="primary" class="ml-2" @click="copyCode(coupon.code)">Copy</v-btn>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <strong>Initial_date</strong>    {{ coupon.start_date }}
                        </v-col>

                        <v-col cols="12" sm="6">
                            <strong>end_date</strong> {{ coupon.end_date }}
                        </v-col>
                        <v-col cols="12" sm="6">
                            <strong>Discount value:</strong> {{ coupon.discount }}%
                        </v-col>
                        <v-divider></v-divider>
                        <v-col>
                            <v-btn @click="removeCoupon(coupon.id)" variant="text">Remove</v-btn>
                        </v-col>

                        
                    </v-row>
                    
                </v-card-text>
                
            </v-card>
        </v-col>
    </v-row>
 
</template>

<script setup>
    import {ref, onMounted} from 'vue';
    import axios from 'axios';
   // import { useToast } from 'vue-toastification' 

    const userId = localStorage.getItem('user_id');
    const coupons = ref([]);
  //  const toast = useToast?.();
    const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

    const getCoupons = async () => {
        try{
            const response = await api.get(`/coupon/get-coupons/${userId}`);
            coupons.value = response.data;
            console.log(coupons);
        }
        catch(e){
            console.log('Erro ao buscar cupons', e);
        }
    }

    const copyCode = async (code) => {
        try{
            await navigator.clipboard.writeText(code)
             alert('código copiado !')
           
        }
        catch(e){
            //toast.error('Erro ao copiar código', e);
              alert('Falha ao copiar')
           
        }
    };

    const removeCoupon = async (couponId) => {
        try{
            const userId = localStorage.getItem('user_id')
            const response = await api.delete(`/coupon/delete-coupons-by-client/${couponId}`, {
                params: {userId}
            });

            return coupon.value = coupon.value.filter(c => c.id !== couponId);

        }
        catch(e){
            alert('erro ao remover coupon', e);
        }
    };
    
    onMounted(() => {
        getCoupons();
    })

</script>