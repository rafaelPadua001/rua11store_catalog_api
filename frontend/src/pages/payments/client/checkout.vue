<template>
  <v-row justify="center">
    <v-col cols="12" sm="12" md="10" lg="10" xl="6">
      <v-card class="pa-4" elevation="0">
        <v-card-text>
          <v-timeline direction="horizontal" line-inset="12">
            <!-- ETAPA 1: Itens -->
            <v-timeline-item fill-dot :color="currentStep === 1 ? 'primary' : 'grey'">
              <template #icon>
                <v-icon :color="currentStep === 1 ? 'primary' : 'grey'">mdi-cart-outline</v-icon>
              </template>

              <template #opposite>
                <div v-if="currentStep === 1">
                  <v-list>
                    <v-list-item v-for="(item, index) in cart.items" :key="index">
                      <v-card class="pa-2 mb-2" elevation="0">
                        <v-avatar size="50">
                          <v-img :src="item.product_image" :alt="item.product_name" cover></v-img>
                        </v-avatar>

                        <strong>{{ item.product_name }}</strong>

                        <v-row dense class="align-center mt-2" no-gutters>
                          <v-col cols="auto">
                            <strong>Quantidade:</strong>
                          </v-col>
                          <v-col cols="auto">
                            <v-text-field
                              v-model.number="item.quantity"
                              type="number"
                              min="1"
                              density="compact"
                              hide-details
                              style="width: 80px;"
                              @click.stop
                              @mousedown.stop
                            />
                          </v-col>
                        </v-row>

                        <v-card-actions>
                          <v-btn color="error" size="small">Remover</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-list-item>

                    <v-card-actions class="justify-space-between mt-2">
                      <v-spacer></v-spacer>
                      <v-btn color="primary" @click="nextStep">Avançar</v-btn>
                    </v-card-actions>
                  </v-list>
                </div>
              </template>

              <h3>Checkout Items</h3>
            </v-timeline-item>

            <!-- ETAPA 2: Endereço -->
            <v-timeline-item :color="currentStep === 2 ? 'success' : 'grey'">
              <template #icon>
                <v-icon :color="currentStep === 2 ? 'success' : 'grey'">mdi-truck-outline</v-icon>
              </template>

              <template #opposite>
                <div v-if="currentStep === 2">
                  <h3>Endereço de Entrega</h3>
                 
                </div>
              </template>

            
              <div v-if="currentStep === 2">
                  <h3>Endereço de Entrega</h3>
                  <v-text-field label="Rua" variant="outlined"></v-text-field>
                  <v-text-field label="Número" variant="outlined"></v-text-field>

                  <v-card-actions class="justify-space-between mt-2">
                    <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                    <v-btn color="primary" @click="nextStep">Avançar</v-btn>
                  </v-card-actions>
                </div>
            </v-timeline-item>

            <!-- ETAPA 3: Pagamento -->
            <v-timeline-item :color="currentStep === 3 ? 'purple' : 'grey'">
              <template #icon>
                <v-icon :color="currentStep === 3 ? 'purple' : 'grey'">mdi-credit-card-outline</v-icon>
              </template>

              <template #opposite>
                <div v-if="currentStep === 3">
                  <h3>Pagamento</h3>
                  <v-text-field label="Número do Cartão" variant="outlined"></v-text-field>

                  <v-card-actions class="justify-space-between mt-2">
                    <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                    <v-btn color="success">Finalizar Pedido</v-btn>
                  </v-card-actions>
                </div>
              </template>

              Confirmar Pagamento
            </v-timeline-item>
          </v-timeline>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const cart = route.query.item ? JSON.parse(route.query.item) : null

const currentStep = ref(1)

// Avançar para a próxima etapa
const nextStep = () => {
  if (currentStep.value < 3) currentStep.value++
}

// Voltar para a etapa anterior
const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--
}
</script>
