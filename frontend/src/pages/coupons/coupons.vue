<template>
    <v-row justify="center" align="center" class="mt-4">
        <v-col cols="12" sm="10" md="10" lg="10" xl="6">
            <v-card class="pa-4">
                <v-card-title>Coupons management</v-card-title>
                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newCoupon" class="mb-2">
                        <v-icon left>mdi-plus</v-icon>
                        Add Coupon
                    </v-btn>
                </v-card-actions>

                <v-data-table 
                    :headers="headers" 
                    :items="coupons" 
                    :items-per-page="10" 
                    class="elevation-1" 
                    item-key="id"
                    fixed-header 
                    height="500" 
                    :loading="loading" 
                    loading-text="Loading coupons...">

                    <!-- Exibe imagens de cupons -->
                    <template v-slot:item.image_path="{ item }">
                        <v-img 
                            v-if="item.image_path" 
                            :src="getCouponImage(item.image_path, item.id)"
                            alt="Imagem do Cupom" 
                            contain 
                            min-width="60" 
                            max-width="70" 
                            min-height="10"
                            class="rounded-lg"
                        ></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small color="primary" @click="editDialog(item)">
                            mdi-pencil
                        </v-icon> 

                        <v-icon small color="error" @click="deleteCoupon(item)">
                            mdi-delete
                        </v-icon> 
                    </template>
                </v-data-table>

                <v-dialog v-model="couponDialog" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">{{ editedIndex === -1 ? 'Criar Cupom' : 'Editar Cupom' }}</span>
                        </v-card-title>

                        <v-card-subtitle>
                            <v-form ref="form" @submit.prevent="submitCoupon" enctype="multipart/form-data">
                                <v-text-field v-model="editedCoupon.title" label="Título do Cupom" required />
                                <v-text-field v-model="editedCoupon.code" label="Código do Cupom" required />
                                <v-text-field v-model="editedCoupon.discount" label="Desconto" required />
                                <v-text-field v-model="editedCoupon.client_id" label="ID do Cliente" required />
                                <v-text-field v-model="editedCoupon.start_date" label="Data de Início" type="date" required />
                                <v-text-field v-model="editedCoupon.end_date" label="Data de Fim" type="date" required />

                                <!-- Upload de Imagem -->
                                <v-file-input 
                                    label="Imagem do Cupom" 
                                    v-model="editedCoupon.image" 
                                    accept="image/*"
                                    prepend-icon="mdi-image" 
                                />
                            </v-form>
                        </v-card-subtitle>

                        <v-card-actions>
                            <v-btn color="primary" @click="submitCoupon">
                                {{ editedIndex === -1 ? 'Criar Cupom' : 'Salvar Alterações' }}
                            </v-btn>
                            <v-btn color="green" text @click="closeDialog">Fechar</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
import axios from "axios";

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
            loading: false,
            headers: [
                { title: "ID", key: "id" },
                { title: "Imagem", key: "image_path" },
                { title: "Título", key: "title" },
                { title: "Código", key: "code" },
                { title: "Desconto", key: "discount" },
                { title: "Cliente ID", key: "client_id" },
                { title: "Init Date", key: "start_date" },
                { title: "End Date", key: "end_date" },
                { title: "Ações", key: "actions", sortable: false }
                
            ],
            couponDialog: false,
            coupons: [],
            editedCoupon: {
                title: '',
                code: '',
                discount: '',
                client_id: '',
                start_date: '',
                end_date: '',
                image: null
            },
            editedIndex: -1,
        };
    },
    created() {
        this.loadCoupons();
    },
    methods: {
        async loadCoupons() {
            this.loading = true;
            const token = localStorage.getItem("user_token");
            if (!token) return this.$router.push("/login");

            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            };
            try {
                const response = await api.get("/coupon/coupons", config);
                this.coupons = response.data;
                console.log(this.coupons);
            } catch (error) {
                console.error("Error loading coupons:", error);
            } finally {
                this.loading = false;
            }
        },
        newCoupon() {
            this.editedCoupon = {
                title: '',
                code: '',
                discount: '',
                client_id: '',
                start_date: '',
                end_date: '',
                image: null
            };
            this.editedIndex = -1;
            this.couponDialog = true;
        },
        closeDialog() {
            this.couponDialog = false;
        },
        async submitCoupon() {
            const formData = new FormData();
            formData.append('title', this.editedCoupon.title);
            formData.append('code', this.editedCoupon.code);
            formData.append('discount', this.editedCoupon.discount);
            formData.append('client_id', this.editedCoupon.client_id);
            formData.append('start_date', this.editedCoupon.start_date);
            formData.append('end_date', this.editedCoupon.end_date);
            if (this.editedCoupon.image) {
                formData.append('image', this.editedCoupon.image);
            }

            const token = localStorage.getItem("user_token");
            if (!token) return this.$router.push("/login");

            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "multipart/form-data",
                },
            };

            try {
                let response;

                if (this.editedIndex === -1) {
                    // Criar novo cupom
                    response = await api.post('/coupon/create_coupon', formData, config);
                } else {
                    // Atualizar cupom existente (supondo que API tenha endpoint PUT /coupon/:id)
                    response = await api.put(`/coupon/${this.editedCoupon.id}`, formData, config);
                    Object.assign(this.coupons[this.editedIndex], response.data.coupon);
                }

                if (response.status === 201 || response.status === 200) {
                    this.couponDialog = false;
                    if (this.editedIndex === -1) {
                        this.coupons.push(response.data.coupon);
                        alert('Cupom criado com sucesso!');
                    } else {
                       // this.coupons.splice(this.editedIndex, 1, response.data.coupon);
                        alert('Cupom atualizado com sucesso!');
                    }
                } else {
                    alert(`Erro: ${response.data.error || 'Ocorreu um erro'}`);
                }
            } catch (err) {
                alert('Erro ao salvar cupom');
                console.error(err);
            }
        },
        getCouponImage(imagePath, couponId = null) {
            if (!imagePath) return "https://via.placeholder.com/300";

            if (imagePath.startsWith('http')) {
                return imagePath.replace('http://', 'https://');
            }

            const baseUrl = window.location.hostname === 'localhost'
                ? 'http://localhost:5000'
                : 'https://rua11store-catalog-api-lbp7.onrender.com';

            let path = imagePath.startsWith('/') ? imagePath : '/' + imagePath;
            return `${baseUrl}${path}`;
        },
        editDialog(item) {
            this.editedCoupon = { ...item, image: null }; // Limpa campo image para upload, para evitar problemas
            this.editedIndex = this.coupons.indexOf(item);
            this.couponDialog = true;
        },
        deleteCoupon(item) {
            if (!confirm(`Deseja realmente deletar o cupom ${item.title}?`)) return;

            const token = localStorage.getItem("user_token");
            if (!token) return this.$router.push("/login");

            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            };

            api.delete(`/coupon/${item.id}`, config)
                .then(() => {
                    const index = this.coupons.indexOf(item);
                    if (index > -1) this.coupons.splice(index, 1);
                    alert('Cupom deletado com sucesso!');
                })
                .catch(err => {
                    alert('Erro ao deletar cupom');
                    console.error(err);
                });
        }
    }
}
</script>
