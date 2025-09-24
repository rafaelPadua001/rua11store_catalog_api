<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12">
            <v-card class="pa-4" elevation="2">
                <v-card-text>
                    <v-textarea v-model="comment" label="Escreva seu comentário..." auto-grow outlined rows="2"
                        class="mb-4" v-if="user">

                    </v-textarea>
                    <p v-else>Faça login para comentar</p>
                    <div class="d-flex flex-column gap-3">
                        <v-checkbox v-model="anonymous" label="Comentar como Anônimo" />

                        <div class="d-flex flex-wrap justify-center gap-2">
                            <v-btn color="red" variant="outlined" @click="login('google')">
                                <v-icon start>mdi-google</v-icon>
                                Google
                            </v-btn>
                            <v-btn color="blue" variant="outlined" @click="login('facebook')">
                                <v-icon start>mdi-facebook</v-icon>
                                Facebook
                            </v-btn>
                            <v-btn color="light-blue" variant="outlined" @click="login('twitter')">
                                <v-icon>mdi-twitter</v-icon>
                                Twitter
                            </v-btn>
                        </div>
                    </div>
                </v-card-text>

                <v-card-actions>
                    <div class="text-right mt-4">
                        <v-btn color="primary" :disabled="!comment" @click="submitComment">
                            Enviar comentário
                        </v-btn>
                    </div>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>

</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { supabase } from "@/supabase";
import axios from 'axios'

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const comment = ref('');
let comments = ref('');
const anonymous = ref(false);
const user = ref(null);
const emit = defineEmits(['create:comment', 'update:user']);

const props = defineProps({
    postId: {
        type: Number,
        required: true,
    }
});

const submitComment = async () => {
    if (!comment.value.trim()) return;

    try {
        let payload;

        if (anonymous.value) {
            payload = {
                post_id: props.postId,
                text: comment.value,
                user_id: null,
                username: null,
                user_avatar: null,
                login_provider: null
            };
        }
        else if (user.value) {
            console.log(user.value)
            payload = {
                post_id: props.postId,
                text: comment.value,
                user_id: user.value.id,
                username: user.value.user_metadata.full_name || user.value.email,
                user_avatar: user.value.user_metadata.avatar_url || null,
                login_provider: user.value.app_metadata?.provider || null
            };
        }
        else {
            console.warn('Precisa logar ou marcar anônimo!');
            return
        }

        const response = await api.post('/post-comment/post-comment', payload);
        const data = response.data.comment;
        emit('create:comment', data);
        clearComment();
    }
    catch (e) {
        console.log('Erro ao enviar comentário:', e.message);
    }
};

const clearComment = () => {
    comment.value = "";
    anonymous.value = false;
};
//Social login
const login = async (provider) => {
    try {
        const currentUrl = window.location.href; // pega a URL atual (com o slug)
        //console.log(currentUrl);
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider,
            options: {
                redirectTo: currentUrl, // volta exatamente para a página do post
            },
        });

        if (error) throw error;
    } catch (err) {
        console.error("Erro no login social:", err.message);
    }
};

onMounted(async () => {
    const { data } = await supabase.auth.getSession();
    if (data.session) {
        user.value = data.session.user;
    }

    supabase.auth.onAuthStateChange((_event, session) => {
        user.value = session?.user || null;
        emit('update:user', user.value);
    });
});
</script>