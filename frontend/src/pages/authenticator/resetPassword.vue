<template>
    <v-alert v-if="!token" type="error" class="mt-4">
        Token de recuperação ausente ou inválido.
    </v-alert>

    <v-spacer></v-spacer>
    <div class="fill-height">
        <v-row justify="center" align="center" class="fill-height">
            <v-col cols="12" sm="8" md="5" lg="4">
                <v-card>
                    <v-card-title class="text-h5 text-center">Reset Password</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                          <v-alert v-if="errorMessage" type="error" class="mt-4" border="start" variant="tonal">
                                {{ errorMessage }}
                            </v-alert>

                            <v-alert v-if="successMessage" type="success" class="mt-4" border="start" variant="tonal">
                                {{ successMessage }}
                            </v-alert>

                        <v-form v-model="formValid" @submit.prevent="submitResetPassword">
                            <v-text-field v-model="password" label="New Password" type="password" :rules="passwordRules"
                                required clearable />
                            <v-text-field v-model="confirmPassword" label="Confirm Password" type="password"
                                :rules="confirmPasswordRules" required clearable />

                          

                            <v-btn :disabled="!formValid || loading" type="submit" color="primary" class="mt-4" block>
                                Reset Password
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

    </div>


</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios';

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const route = useRoute()
const router = useRouter()

const token = ref('')
const isValidToken = ref(false)

const password = ref('')
const confirmPassword = ref('')
const formValid = ref(false)
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')


onMounted(() => {
    token.value = route.query.token

    if (!token.value) {
        router.push('/token-invalido')
    }
})

// Regras para a senha: obrigatório, min 6 caracteres
const passwordRules = [
    (v) => !!v || 'Senha é obrigatória',
    (v) => v.length >= 6 || 'Senha deve ter pelo menos 6 caracteres',
]

// Regras para confirmação: obrigatório e igual à senha
const confirmPasswordRules = [
    (v) => !!v || 'Confirmação da senha é obrigatória',
    (v) => v === password.value || 'Senhas não coincidem',
]

const submitResetPassword = async () => {
    loading.value = true
    successMessage.value = ''
    errorMessage.value = ''

    try {
        // Simula chamada API
        //await new Promise((resolve) => setTimeout(resolve, 2000))
        const response = await api.post('/auth/resetPassword', { newPassword: password.value, token: token.value });
        // Aqui você faria a chamada real para backend enviando a senha nova

        successMessage.value = 'Senha redefinida com sucesso!'
        password.value = ''
        confirmPassword.value = ''
    } catch (err) {
        errorMessage.value = 'Erro ao redefinir a senha. Tente novamente.'
    } finally {
        loading.value = false
    }
}
</script>
