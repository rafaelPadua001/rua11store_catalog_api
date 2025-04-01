<template>
    <v-card class="mx-auto justify-center" width="400">
        <template v-slot:title>
            <div class="text-center font-weight-black">Rua11Store</div>
        </template>
        <v-divider></v-divider>
        <v-card-text>
            <v-form ref="form" @submit.prevent="login">
                <v-container>
                    <v-row justify="center">
                        <v-col cols="12" md="10" sm="4">
                            <v-text-field v-model="email" :rules="emailRules" label="User email"
                                prepend-inner-icon="mdi-email" required></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-col cols="12" md="10" sm="4">
                            <v-text-field v-model="password" :rules="passwordRules" label="Password" type="password"
                                prepend-inner-icon="mdi-lock" required></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-col cols="auto">
                            <v-btn variant="text" color="primary">
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

                </v-container>
            </v-form>
        </v-card-text>
    </v-card>
</template>

<script setup>
import { ref } from "vue";
import axios from 'axios';

// Campos do formulário
const email = ref("");
const password = ref("");
const form = ref(null);
const loading = ref(false); // Estado para mostrar o spinner no botão
const router = useRouter();

const goToRegister = () => {

    router.push('/authenticator/register');
}

// const goToLogin = () => {
//   drawer.value = false; // Fecha o menu lateral
//   router.push('/authenticator/login'); // Redireciona para a página de login
// };

// Validações
const emailRules = [
    (v) => !!v || "E-mail é obrigatório",
    (v) => /.+@.+\..+/.test(v) || "E-mail inválido",
];

const passwordRules = [
    (v) => !!v || "Senha é obrigatória",
    (v) => v.length >= 8 || "A senha deve ter pelo menos 8 caracteres",
];

// Função de Login
const login = async () => {
    if (!form.value) return; // Evita erro caso `form` não esteja carregado
    const { valid } = await form.value.validate();

    if (valid) {
        loading.value = true; // Ativa o loading no botão
        try {
            const response = await axios.post('https://rua11storecatalogapi-production.up.railway.app/auth/login', {
                email: email.value,
                password: password.value,
            });


            if (response.data.message == "Login realizado com sucesso!") {
                localStorage.setItem('user_token', response.data.token)
                window.dispatchEvent(new Event("storage"));

                router.push('/authenticator/dashboard');
            }
        } catch (error) {
            console.log('Erro no login:', error);
            alert('Credenciais inválidas ou erro no servidor');
        }
        finally {
            loading.value = false;
            router.push('/authenticator/dashboard');

        }
        // Simula um delay para processamento do login
        // setTimeout(() => {
        //     loading.value = false; // Desativa o loading após 2s
        //     // alert("Login realizado com sucesso!");
        // }, 2000);
    }
};
</script>
