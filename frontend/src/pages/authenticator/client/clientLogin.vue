<template>
    <v-container class="fill-height d-flex align-center justify-center">
        <v-row justify="center">
            <v-col cols="12" sm="8" md="6" lg="4">
               
                <v-card class="pa-2">
                     <template v-slot:title>
                    <div class="text-center" v-if="logoUrl">
                        <v-img :src="logoUrl" alt="logo" width="120" contain class="mx-auto"></v-img>
                    </div>
                </template>
                    <v-card-text>
                        <v-form ref="form" @submit.prevent="login">
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="email" :rules="emailRules" label="User email"
                                        prepend-inner-icon="mdi-email" required></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col>
                                    <v-text-field v-model="password" :rules="passwordRules" label="Password"
                                        type="password" prepend-inner-icon="mdi-lock" required></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row justify="center">
                                <v-col cols="auto">
                                    <v-btn variant="text" color="primary" @click="goToRecovery">
                                        Recovery password
                                    </v-btn>
                                </v-col>
                            </v-row>

                                <v-row justify="center" @click="goToRegister()">
                        <v-col cols="auto">
                            <v-btn variant="text" color="primary">
                                Register
                            </v-btn>
                        </v-col>
                    </v-row>
                

                            <v-row justify="center">
                                <v-col cols="auto">
                                    <v-btn color="primary" type="submit" :loading="loading" :disabled="loading">
                                        <v-icon v-if="!loading" icon="mdi-login"></v-icon>
                                        <span v-if="!loading">Sign up</span>
                                        <span v-else>Loading...</span>
                                    </v-btn>
                                </v-col>
                            </v-row>


                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>

</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from 'axios';


const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

// Campos do formulário
const email = ref("");
const password = ref("");

const form = ref(null);
const loading = ref(false); // Estado para mostrar o spinner no botão
const router = useRouter();
const logoUrl = ref('');

const goToRegister = () => {

    router.push('/authenticator/client/clientRegister');
}

 const goToLogin = () => {
   drawer.value = false; // Fecha o menu lateral
   router.push('/authenticator/login'); // Redireciona para a página de login
 };

const goToRecovery = () => {
    router.push('/authenticator/recoveryPassword');
}

// Validações
const emailRules = [
    (v) => !!v || "E-mail é obrigatório",
    (v) => /.+@.+\..+/.test(v) || "E-mail inválido",
];

const passwordRules = [
    (v) => !!v || "Senha é obrigatória",
    (v) => v.length >= 8 || "A senha deve ter pelo menos 8 caracteres",
];

onMounted(async () => {
    try {
        const res = await api.get('/config/config');
        logoUrl.value = res.data.logo_url;
    } catch (err) {
        console.error("Erro ao carregar logo:", err);
    }
});

// Função de Login
const login = async () => {
    if (!form.value) return; // Evita erro caso `form` não esteja carregado
    const { valid } = await form.value.validate();

    if (valid) {
        loading.value = true; // Ativa o loading no botão
        try {
            const response = await api.post('/client/loginClient', {
                email: email.value,
                password: password.value,
            });

            const token = response.data.token;
            const userId = response.data.user?.id;

            if (response.data.message == "Login realizado com sucesso!") {
                localStorage.setItem('user_id', userId)
                localStorage.setItem('token', token);
                localStorage.setItem('refresh_token', response.data.refresh_token)
                window.dispatchEvent(new Event("storage"));
                
                return router.push('/authenticator/client/clientDashboard');
            }
        } catch (error) {
            console.log('Erro no login:', error);
            alert('Credenciais inválidas ou erro no servidor');
            return false;
        }
        finally {
            loading.value = false;
        }
    }
};

</script>
