<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" md="12">
            <v-card>
                <v-toolbar flat>
                    <v-toolbar-title class="text-body-1">
                        Denunciar comentário ?
                    </v-toolbar-title>

                    <v-spacer></v-spacer>

                    <v-btn icon="mdi-close" @click="closeDialog()"></v-btn>
                </v-toolbar>
                <v-card-text>
                    <div>
                        <v-row justify="center">
                            <v-col cols="4" sm="4" class="d-flex justify-center">
                                <v-img
                                    :src="props.comment.user_avatar || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'"
                                    class="rounded-circle" contain></v-img>


                            </v-col>

                            <v-col cols="8" sm="8">
                                <div>
                                    {{ props.comment.username }}
                                </div>
                                <div>
                                    {{ props.comment.text }}
                                </div>
                                <div>
                                    <v-chip size="x-small">
                                        {{ props.comment.login_provider }}
                                    </v-chip>
                                </div>
                            </v-col>
                        </v-row>
                    </div>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions class="d-flex justify-end">
                    <v-btn variant="elevated" color="primary" size="small" @click="submitReport(props.comment)">
                        Confirmar
                    </v-btn>
                    <v-btn variant="elevated" color="grey" size="small" @click="closeDialog()">
                        cancelar
                    </v-btn>
                </v-card-actions>
            </v-card>


        </v-col>
    </v-row>
</template>

<script setup>
import axios from 'axios';

const showToast = ref(false);
const toastMessage = ref('');

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const emit = defineEmits(['closeReportDialog']);

const props = defineProps({
    comment: {
        type: Object,
        required: true
    }
});

const closeDialog = async () => {
    emit('closeReportDialog');
};

const submitReport = async (comment) => {
    try {
        const response = api.post(`/post-comment/post-comment/post-comment-report/${comment.id}`);
        emit('closeReportDialog', props.comment.id);
    }
    catch (e) {
        console.log('Erro ao reportar comentário:', e.message);
        emit('closeReportDialog', 'Erro ao enviar reporte.', true);
    }
}
</script>