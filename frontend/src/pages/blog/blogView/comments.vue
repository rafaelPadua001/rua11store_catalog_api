<template>
    <v-row justify="center">
        <v-col>
            <v-card>
                <v-data-table :items="comments">

                </v-data-table>
            </v-card>
        </v-col>
    </v-row>
   
  <!--  {{ comments }} -->
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const comments = ref([]);

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const getPostComments = async () => {
    try{
        const response = await api.get('/post-comment/post-comment');
        const data = response.data;
        comments.value.push(...response.data);
        console.log(data);

    }
    catch(e){
        console.log('Erro ao buscar comentários:', e.message);
    }
};

onMounted(async () => {
    getPostComments();
});

</script>