<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="text-h6 justify-center">Recuperar Senha</v-card-title>
          <v-divider class="my-2" />

          <v-card-text>
            <v-form v-model="formValid" @submit.prevent="submitRecovery">
              <v-alert
                v-if="successMessage"
                type="success"
                class="mb-4"
                border="start"
                variant="tonal"
              >
                {{ successMessage }}
              </v-alert>

              <v-alert
                v-else-if="errorMessage"
                type="error"
                class="mb-4"
                border="start"
                variant="tonal"
              >
                {{ errorMessage }}
              </v-alert>

              <v-text-field
                v-model="email"
                label="E-mail"
                :rules="emailRules"
                type="email"
                required
                clearable
              />

              <v-btn
                :disabled="!formValid || loading"
                :loading="loading"
                type="submit"
                color="primary"
                class="mt-4"
                block
              >
                Enviar E-mail de Recuperação
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const email = ref('');
const formValid = ref(false);
const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const emailRules = [
  (v) => !!v || 'E-mail é obrigatório',
  (v) => /.+@.+\..+/.test(v) || 'E-mail deve ser válido',
];

const submitRecovery = async () => {
  loading.value = true;
  successMessage.value = '';
  errorMessage.value = '';

  try {
    // Simula requisição à API
   // await new Promise((resolve) => setTimeout(resolve, 2000));
    const response = await api.post('/auth/recoveryPassword', { email: email.value });
    successMessage.value = 'E-mail de recuperação enviado com sucesso!';
    email.value = '';
  } catch (error) {
    errorMessage.value = 'Erro ao enviar o e-mail de recuperação. Tente novamente.';
  } finally {
    loading.value = false;
  }
};
</script>
