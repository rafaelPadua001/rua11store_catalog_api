
    <template>
    <v-card class="mx-auto justify-center" width="400">
        <v-toolbar color="transparent">
            <v-toolbar-title>Register</v-toolbar-title>
        </v-toolbar>

        <v-divider></v-divider>

        <v-card-text>
            <template v-slot:title>
            <div class="text-center" v-if="logoUrl">
                <v-img :src="logoUrl" alt="logo" width="120" contain class="mx-auto"></v-img>
            </div>
        </template>
            <v-form ref="form" @submit.prevent="register">
                <v-container>
                    <v-row justify="center">
                        <v-col cols="12" md="10" sm="4">
                            <v-text-field v-model="name" :rules="nameRules" label="Full Name"
                                prepend-inner-icon="mdi-account" required></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-col cols="12" md="10" sm="4">
                            <v-text-field v-model="birthDate" :rules="birthDateRules" label="Birth Date" type="date"
                                prepend-inner-icon="mdi-calendar" required></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-col cols="12" md="10" sm="4">
                            <v-text-field v-model="email" :rules="emailRules" label="User Email"
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
                        <v-col cols="12" md="10" sm="4">
                            <v-text-field v-model="confirmPassword" :rules="confirmPasswordRules"
                                label="Confirm Password" type="password" prepend-inner-icon="mdi-lock-check"
                                required></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-col cols="auto">
                            <v-btn color="primary" type="submit" :loading="loading" :disabled="loading">
                                <v-icon v-if="!loading" icon="mdi-account-plus"></v-icon>
                                <span v-if="!loading">Register</span>
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
import { useRouter } from "vue-router";
import axios from 'axios';

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const logoUrl = ref('');
const router = useRouter();
const form = ref(null);
const loading = ref(false);

// Campos do formulário
const name = ref("");
const birthDate = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

// Regras de validação
const nameRules = [(v) => !!v || "Nome é obrigatório"];

const birthDateRules = [
    (v) => !!v || "Data de nascimento é obrigatória",
    (v) => /^\d{4}-\d{2}-\d{2}$/.test(v) || "Data inválida (use o formato YYYY-MM-DD)",
    (v) => isAdult(v) || "Você precisa ter pelo menos 18 anos para se registrar",
];

onMounted(async () => {
    try {
        const res = await api.get('/config/config');
        logoUrl.value = res.data.logo_url;
    } catch (err) {
        console.error("Erro ao carregar logo:", err);
    }
});


// Função para verificar se o usuário tem 18 anos ou mais
const isAdult = (birthDate) => {
    if (!birthDate) return false;

    const birth = new Date(birthDate);
    const today = new Date();

    // Calcula a idade do usuário
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    const dayDiff = today.getDate() - birth.getDate();

    // Ajusta a idade se o mês ou dia do aniversário ainda não ocorreu no ano atual
    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--;
    }

    return age >= 18;
};

const emailRules = [
    (v) => !!v || "E-mail é obrigatório",
    (v) => /.+@.+\..+/.test(v) || "E-mail inválido",
];

const passwordRules = [
    (v) => !!v || "Senha é obrigatória",
    (v) => v.length >= 8 || "A senha deve ter pelo menos 8 caracteres",
];

const confirmPasswordRules = [
    (v) => !!v || "Confirmação de senha é obrigatória",
    (v) => v === password.value || "As senhas não coincidem",
];

// Função para registrar usuário
const register = async () => {
    if (!form.value) return;
    const { valid } = await form.value.validate();

    if (valid) {
        loading.value = true;

        console.log("Nome:", name.value);
        console.log("Data de Nascimento:", birthDate.value);
        console.log("Email:", email.value);
        console.log("Senha:", password.value);
        try {
            const response = await api.post('/client/registerClient', {
                name: name.value,
                birthDate: birthDate.value,
                email: email.value,
                password: password.value,
                type: 'client'
            });

            router.push('/authenticator/client/clientLogin');

        } catch (error) {
            alert(error.message);
        }
        finally {
            loading.value = false;
        }
    }
};
</script>
