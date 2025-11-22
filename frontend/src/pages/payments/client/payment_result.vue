<template>
  <v-row justify="center" class="my-6">
    <v-col :cols="12" :md="6">
      <v-card
        class="pa-6 text-center"
        elevation="3"
      >
        <v-icon
          :color="status === 'approved' ? 'green' : status === 'pending' ? 'amber darken-2' : 'red darken-2'"
          size="56"
          class="mb-4"
        >
          {{ status === 'approved' ? 'mdi-check-circle-outline' : status === 'pending' ? 'mdi-clock-outline' : 'mdi-close-circle-outline' }}
        </v-icon>

        <v-card-title class="text-h5 font-weight-bold mb-2">
          {{ status }}
        </v-card-title>

        <v-card-text class="text-body-1">
          {{ message }}
        </v-card-text>

        <v-card-actions class="justify-center mt-4">
          <v-btn color="primary" :to="'/'">Voltar para a loja</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const status = ref('')
const message = ref('')

onMounted(() => {
  status.value = localStorage.getItem('paymentStatus')
  message.value = localStorage.getItem('paymentMessage')
})
</script>
