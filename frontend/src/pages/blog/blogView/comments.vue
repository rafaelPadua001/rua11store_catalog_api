<template>
    <v-row justify="center">
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>Comments management</h5>
                </v-card-title>
                <v-divider></v-divider>

                <v-data-table :headers="headers" :items="comments" items-per-page="10" class="elevation-0" item-key="id"
                    fixed-header height="500" :loading="loading" loading-text="Loading coupons...">

                    <template v-slot:item.user_avatar="{ item }">
                        <v-avatar>
                            <v-img :src="item.user_avatar" :alt="item.user_avatar" class="rounded-circle"
                                width="35"></v-img>
                        </v-avatar>


                    </template>
                    <template v-slot:item.login_provider="{ item }">

                        <v-chip v-if="item.login_provider == 'email'" color="grey">{{ item.login_provider }}</v-chip>
                        <v-chip v-if="item.login_provider == 'facebook'" color="primary">{{ item.login_provider
                            }}</v-chip>
                    </template>
                    <template v-slot:item.username="{ item }">

                        {{ item.username }}

                    </template>
                    <template v-slot:item.status="{ item }">
                        <v-chip color="primary" v-if="item.status == 'pending'">
                            {{ item.status }}
                        </v-chip>
                        <v-chip color="success" v-else-if="item.status == 'active'">
                            {{ item.status }}
                        </v-chip>
                        <v-chip color="warning" v-else-if="item.status == 'reported'">
                            {{ item.status }}
                        </v-chip>
                        <v-chip color="error" v-else>
                            {{ item.status }}
                        </v-chip>

                    </template>

                    <template v-slot:item.created_at="{ item }">
                        {{ new Date(item.created_at).toLocaleDateString('pt-BR') }}
                    </template>

                    <template v-slot:item.updated_at="{ item }">
                        {{ new Date(item.updated_at).toLocaleDateString('pt-BR') }}
                    </template>

                    <template v-slot:item.actions="{ item }">
                        <v-icon small color="primary" @click="editDialog(item)">
                            mdi-pencil
                        </v-icon>

                        <v-icon small color="error" @click="deleteComment(item)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>
            </v-card>

            <v-dialog v-model="editCommentDialog" max-width="870">
                <v-card>
                    <v-card-text>
                        <div>
                            <v-row justify="center">
                                <v-col cols="4" sm="2" class="d-flex justify-center">
                                    <v-avatar size="90">
                                        <v-img
                                            :src="editedComment.user_avatar || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'"
                                            class="rounded-circle"></v-img>
                                    </v-avatar>
                                </v-col>

                                <v-col cols="8" sm="8">
                                    <div>
                                        {{ editedComment.username }}
                                    </div>
                                    <div>
                                        {{ editedComment.text }}
                                    </div>
                                    <div>
                                        <v-chip size="x-small">
                                            {{ editedComment.login_provider }}
                                        </v-chip>
                                    </div>

                                    <div>
                                        <v-select v-model="editedComment.status" :items="statusOptions" label="Status"
                                            outlined></v-select>

                                    </div>
                                </v-col>

                                <v-divider></v-divider>
                            </v-row>
                        </div>
                    </v-card-text>

                    <v-card-actions>
                        <v-btn color="primary" @click="confirmEdit(editedComment)">
                            Confirmar
                        </v-btn>
                        <v-btn color="gray" @click="close()">
                            Cancelar
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import commentInputForm from '../../comments/commentsView/commentInputForm.vue';

const comments = ref([]);
const editCommentDialog = ref(false);
const editedComment = ref('');
const statusOptions = ["active", "removed", "pending"];

const headers = [
    { title: "Id", key: "id", align: "start" },
    { title: "postId", key: "post_id", align: "start" },
    { title: "avatar", key: "user_avatar" },
    { title: "Name", key: "username", align: "start" },
    { title: "comment", key: "text" },
    { title: "Provider", key: "login_provider" },
    { title: "status", key: 'status' },
    { title: "created", key: "created_at" },
    { title: "updated", key: "updated_at" },
    { title: "Actions", key: "actions", sortable: false }

];

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const getPostComments = async () => {
    try {
        const response = await api.get('/post-comment/post-comment');
        const data = response.data;
        comments.value.push(...response.data);
    }
    catch (e) {
        console.log('Erro ao buscar comentários:', e.message);
    }
};

const editDialog = async (comment) => {
    editCommentDialog.value = true;
    editedComment.value = { ...comment };
}

const confirmEdit = async (comment) => {
    try {
        const response = await api.post(`/post-comment/post-comment/comment-alter-status/${comment.id}`, { 'status': comment.status })
        const data = response.data;

        const index = comments.value.findIndex(c => c.id === comment.id);
        if (index !== -1) {
            comments.value[index].status = comment.status;
        }
        close();
    }
    catch (e) {
        console.log('Erro ao alterar status', e.message);
    }
}

const close = async () => {
    editCommentDialog.value = false;
    editedComment.value = '';
}

const deleteComment = async (comment) => {
    if (!confirm("Tem certeza que deseja remover este comentário permanentemente ?")) return;

    try {

        await api.delete(`/post-comment/post-comment/${comment.id}`);
        //Remove comment from local list
        comments.value = comments.value.filter(c => c.id !== comment.id);
    }
    catch (error) {
        console.log("Error deleting product:", error);
        //   this.$toast.error("Erro ao excluir produto");
    }
}

onMounted(async () => {
    getPostComments();
});

</script>