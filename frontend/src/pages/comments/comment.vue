<template>
    <v-row justify="center" align="center" class="mt-4">
        <v-col cols="12" sm="10" md="10" lg="10" xl="6">
            <v-card class="pa-4">
                <v-card-title>Comments management</v-card-title>
                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newComment" class="mb-2">
                        <v-icon left>mdi-plus</v-icon>
                        Add Coupon
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="comments" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading coupons...">

                    <!-- Exibe imagens de cupons 
                    <template v-slot:item.image_path="{ item }">
                        <v-img v-if="item.image_path" :src="getCouponImage(item.image_path, item.id)"
                            alt="Imagem do Cupom" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template> -->

                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small color="primary" @click="editDialog(item)">
                            mdi-pencil
                        </v-icon>

                        <v-icon small color="error" @click="deleteComment(item)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>

                <v-dialog v-model="commentDialog" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">{{ editedIndex === -1 ? 'Criar Comentário' : 'Editar Comentário'
                            }}</span>
                        </v-card-title>

                        <v-card-subtitle>
                            <v-form ref="form" @submit.prevent="submitComment">
                                <!-- Campo de comentário -->
                                <v-textarea v-model="editedComment.comment" label="Comentário" required rows="3"
                                    auto-grow />

                                <!-- Produto relacionado -->
                                <v-text-field v-model="editedComment.product_id" label="ID do Produto" required
                                    type="number" />

                                <v-text-field v-model="editedComment.user_id" label="ID do Produto" required
                                    type="number" />

                                <v-text-field v-model="editedComment.user_name" label="ID do Produto" required
                                    type="text" />
                                <!-- Status do comentário -->
                                <v-select v-model="editedComment.status" :items="['ativo', 'pendente', 'removido']"
                                    label="Status" required />
                            </v-form>
                        </v-card-subtitle>

                        <v-card-actions>
                            <v-btn color="primary" @click="submitComment">
                                {{ editedIndex === -1 ? 'Criar Comentário' : 'Salvar Alterações' }}
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
                { title: "User ID", key: "user_id" },
                { title: "User Name", key: "user_name" },
                { title: "Product ID", key: "product_id" },
               // { title: "Title", key: "title" },
                { title: "Comment", key: "comment" },
                { title: "Created At", key: "created_at" },
                { title: "Updated At", key: "updated_at" },
                { title: "Actions", key: "actions", sortable: false }
            ],

            commentDialog: false,
            comments: [],
            editedIndex: -1,
            editedComment: {}
        };
    },
    created() {
        this.loadComments();
    },
    methods: {
        async loadComments() {
            this.loading = true;
            const token = localStorage.getItem("user_token");
            if (!token) return this.$router.push("/login");

            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            };
            try {
                const response = await api.get("/comments/comments", config);
                this.comments = response.data;
                console.log(this.comments);
            } catch (error) {
                console.error("Error loading coupons:", error);
            } finally {
                this.loading = false;
            }
        },
        newComment() {
            this.editedComment = { comment: '', product_id: null, status: 'pendente', user_id: '' }
            this.editedIndex = -1
            this.commentDialog = true
        },
        closeDialog() {
            this.commentDialog = false;
        },
        async submitComment() {
            try {
                const token = localStorage.getItem('user_token');

                if (!token) return this.$router.push('/login');

                const config = { headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } };


                let payload = { ...this.editedComment };
                if (typeof payload.is_subcategory === 'object' && payload.is_subcategory !== null) {
                    payload.is_subcategory = payload.is_subcategory.key;
                }

                let response;
                if (this.editedIndex === -1) {
                    response = await api.post('/comments/new', payload, config);
                    this.commentDialog = false;
                    return this.comments.push(response.data.comment);
                } else {
                    response = await api.put(`/comments/update/${this.editedComment.id}`, payload, config);
                    Object.assign(this.comments[this.editedIndex], response.data.comments);
                }
                this.close();
            } catch (error) {
                console.error("Error saving category:", error.response?.data || error.message);
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
            this.editedComment = { ...item, image: null }; // Limpa campo image para upload, para evitar problemas
            this.editedIndex = this.comments.indexOf(item);
            this.commentDialog = true;
        },
        deleteComment(item) {
            if (!confirm(`Deseja realmente deletar o cupom ${item.comment}?`)) return;
    
            const token = localStorage.getItem("user_token");
            if (!token) return this.$router.push("/login");
    
            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            };
    
            api.delete(`/comments/delete/${item.id}`, config)
                .then(() => {
                    const index = this.comments.indexOf(item);
                    if (index > -1) this.comments.splice(index, 1);
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
