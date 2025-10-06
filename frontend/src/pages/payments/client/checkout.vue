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
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-list>
                        <v-list-item v-for="(item, index) in cart.items" :key="index">
                          <v-row>
                            <v-col>

                            </v-col>
                          </v-row>
                          <v-card class="pa-2 mb-2" elevation="0">
                            <v-avatar size="50">
                              <v-img :src="item.product_image" :alt="item.product_name" cover></v-img>
                            </v-avatar>
                            <v-row>
                              <v-col cols="auto">
                                <strong>{{ item.product_name }}</strong>
                              </v-col>
                              <v-col cols="auto">
                                <strong>R$ {{ item.product_price }}</strong>
                              </v-col>
                            </v-row>

                            <v-row dense class="align-center mt-2" no-gutters>
                              <v-col cols="auto">
                                <strong>Qtd:</strong>
                              </v-col>
                              <v-col cols="auto">
                                <v-text-field v-model.number="item.quantity" type="number" min="1" density="compact"
                                  hide-details style="width: 80px;" @click.stop @mousedown.stop />
                              </v-col>
                              <v-col cols="auto">
                                <strong>R$ {{ (Number(item.quantity) * Number(item.product_price)).toFixed(2)
                                  }}</strong>
                              </v-col>
                            </v-row>

                            <v-card-actions>
                              <v-btn color="error" size="small">Remover</v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-list-item>
                      </v-list>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-card>
                        <v-card-title>
                          Resumo
                        </v-card-title>
                        <v-card-text>
                          <v-row>
                            <v-col cols="auto">
                              <strong>Total em produtos:</strong>
                            </v-col>
                            <v-col cols="auto">
                              R$ {{ totalCarrinho.toFixed(2) }}
                            </v-col>
                          </v-row>
                             
                           <v-row justify="stretch">
    <v-col cols="12" md="8" sm="4">
      
      <!-- Alterna entre select e input -->
      <div class="d-flex align-center">
        <div class="flex-grow-1">
          <v-select
            v-if="!useTextInput"
            v-model="selectedCoupon"
            :items="formattedCoupons"
            item-title="displayText"
            item-value="id"
            label="Selecione um cupom"
            outlined
            dense
            :menu-props="{ maxHeight: '300px' }"
            return-object
          ></v-select>

          <v-text-field
            v-else
            v-model="couponText"
            label="Digite o cupom"
            outlined
            dense
          ></v-text-field>
        </div>

        <!-- Botão para alternar -->
        <v-btn
          text
          class="ms-2"
          @click="useTextInput = !useTextInput"
        >
          {{ useTextInput ? 'Selecionar' : 'Digitar' }}
        </v-btn>
      </div>

    </v-col>
  </v-row>
                          
                          <!-- Exibir cupom aplicado 
                          <v-row v-if="selectedCoupon" class="mt-2">
                            <v-col cols="12">
                              <v-alert type="success" density="compact">
                                Cupom aplicado: <strong>{{ selectedCoupon.label }}</strong> 
                                ({{ selectedCoupon.discount }}% de desconto) - 
                                Válido até {{ formatDate(selectedCoupon.end_date) }}
                              </v-alert>
                            </v-col>
                          </v-row>-->

                          <v-row justify="end" class="mt-2">
                            <v-col cols="auto">
                              <v-btn 
                                color="success" 
                                @click="applyCoupon"
                                :disabled="!selectedCoupon && !couponText"
                              >
                                Aplicar cupom
                              </v-btn>
                            </v-col>
                          </v-row>

                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>

                <v-btn color="primary" @click="nextStep">Avançar</v-btn>
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
                <v-text-field v-model="cep" label="CEP" variant="outlined" @blur="buscarCep" :loading="loading"
                  maxlength="9" placeholder="00000-000"></v-text-field>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

const route = useRoute()
const cartData = route.query.item ? JSON.parse(route.query.item) : { items: [] }
const coupons = ref([]);
const selectedCoupon = ref(null);
const appliedCoupon = ref(null);
const useTextInput = ref(false)
const couponText = ref('')  

// 👇 Faz o Vue reagir a mudanças no carrinho
const cart = reactive(cartData)

const currentStep = ref(1)

const nextStep = () => {
  if (currentStep.value < 3) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--
}

const totalCarrinho = computed(() => {
  if (!cart.items || !Array.isArray(cart.items)) return 0
  return cart.items.reduce((acc, item) => {
    const price = Number(item.product_price)
    const quantity = Number(item.quantity)
    return acc + (isNaN(price) || isNaN(quantity) ? 0 : price * quantity)
  }, 0)
})

const totalComDesconto = computed(() => {
  if (!appliedCoupon.value || !appliedCoupon.value.discount) {
    return totalCarrinho.value;
  }
  
  const desconto = (totalCarrinho.value * appliedCoupon.value.discount) / 100;
  return totalCarrinho.value - desconto;
})

const formattedCoupons = computed(() => {
  return coupons.value.map(coupon => ({
    ...coupon,
    displayText: `${coupon.label} - Válido até ${formatDate(coupon.end_date)}`
  }));
});
const formatDate = (dateString) => {
  if (!dateString) return ''
  const [year, month, day] = dateString.split('T')[0].split('-')
  return `${day}/${month}/${year}`
}

const getCoupon = async () => {
  try {
    const response = await api.get(`/coupon/get-coupons/${cart.user_id}`)
   
    if(!response.data || response.data.length === 0){
      console.log('Você não possui cupom');
      coupons.value = [];
      return;
    }

    coupons.value = response.data.map(c => ({
      id: c.id,
      label: c.title,
      discount: c.discount,
      start_date: c.start_date,
      end_date: c.end_date,
    }));
    
    //console.log('Cupons carregados:', coupons.value);
  } catch(e) {
    console.log("Erro ao carregar cupons, tente novamente mais tarde", e);
  }
}

const applyCoupon = () => {
  if (useTextInput.value) {
    if (!couponText.value) return
    console.log('Cupom digitado:', couponText.value)
    alert(`Cupom "${couponText.value}" aplicado!`)
    couponText.value = ''
  } else {
    if (!selectedCoupon.value) return

    // Verifica se o cupom expirou
    const now = new Date()
    const endDate = new Date(selectedCoupon.value.end_date)
    if (endDate < now) {
      alert(`O cupom "${selectedCoupon.value.title}" já expirou em ${formatDate(selectedCoupon.value.end_date)}!`)
      return
    }

    // Cupom válido
    appliedCoupon.value = selectedCoupon.value
    console.log('Cupom selecionado:', appliedCoupon.value)
    alert(`Cupom "${selectedCoupon.value.displayText}" aplicado com sucesso!`)
    selectedCoupon.value = null
  }
}

onMounted(async () => {
  await getCoupon();
});
</script>