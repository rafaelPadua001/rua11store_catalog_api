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
                              <strong>Subtotal em produtos:</strong>
                            </v-col>
                            <v-col cols="auto">
                              R$ {{ totalCarrinho.toFixed(2) }}
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col>
                              <strong>Total com desconto (%):</strong>
                            </v-col>
                            <v-col v-if="appliedCoupon && appliedCoupon.discount">

                              R$ {{ (totalCarrinho - (totalCarrinho * appliedCoupon.discount / 100)).toFixed(2) }}
                            </v-col>

                          </v-row>
                          <v-row>
                            <v-col>
                              <strong>Total:</strong>
                            </v-col>
                            <v-col>
                              R$ {{
                                appliedCoupon && appliedCoupon.discount
                                  ? (totalCarrinho - (totalCarrinho * appliedCoupon.discount / 100)).toFixed(2)
                                  : totalCarrinho.toFixed(2)
                              }}
                            </v-col>
                          </v-row>


                          <v-row justify="stretch">
                            <v-col cols="12" md="8" sm="4">

                              <!-- Alterna entre select e input -->
                              <div class="d-flex align-center">
                                <div class="flex-grow-1">
                                  <v-select v-if="!useTextInput" v-model="selectedCoupon" :items="formattedCoupons"
                                    item-title="displayText" item-value="id" label="Selecione um cupom" outlined dense
                                    :menu-props="{ maxHeight: '300px' }" return-object></v-select>

                                  <v-text-field v-else v-model="couponText" label="Digite o cupom" outlined
                                    dense></v-text-field>
                                </div>

                                <!-- Botão para alternar -->
                                <v-btn text class="ms-2" @click="useTextInput = !useTextInput">
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
                              <v-btn color="success" @click="applyCoupon" :disabled="!selectedCoupon && !couponText">
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

                <addressForm ref="addressFormRef" v-if="!address" />
                <v-card v-else>
                  <v-card-text>
                    <div><strong>CEP:</strong> {{ address.cep }}</div>
                    <div><strong>Logradouro:</strong> {{ address.logradouro }}</div>
                    <div><strong>Número:</strong> {{ address.numero }}</div>
                    <div v-if="address.complemento"><strong>Complemento:</strong> {{ address.complemento }}</div>
                    <div><strong>Bairro:</strong> {{ address.bairro }}</div>
                    <div><strong>Cidade:</strong> {{ address.cidade }}</div>
                    <div><strong>Estado:</strong> {{ address.estado }}</div>
                    <div><strong>País:</strong> {{ address.pais }}</div>
                    <div v-if="address.referencia"><strong>Referência:</strong> {{ address.referencia }}</div>
                  </v-card-text>

                  <v-card-actions>
                    <v-btn>Editar</v-btn>
                    <v-btn>Remover</v-btn>
                  </v-card-actions>
                </v-card>
                <v-card-actions class="justify-space-between mt-2">
                  <v-btn color="primary" @click="calculateDelivery">Calcular Frete</v-btn>
                </v-card-actions>

                <div v-if="availableDeliveries.length" class="mt-4">
                  <h4 class="mb-2">Opções de entrega</h4>

                  <v-radio-group v-model="selectedDelivery" class="pa-2">
                    <v-radio v-for="(option, index) in availableDeliveries" :key="index" :value="option" class="my-2">
                      <template #label>
                        <div class="d-flex align-center gap-3">
                          <!-- Logo -->
                          <v-img v-if="option.company.picture" :src="option.company.picture"
                            alt="Logo {{ option.company.name }}" max-width="50" max-height="30" contain
                            class="rounded-sm"></v-img>

                          <!-- Dados da entrega -->
                          <div class="d-flex flex-column">
                            <span class="font-weight-medium">
                              {{ option.company.name }} — R$ {{ option.price }}
                            </span>
                            <small class="text-grey">
                              Prazo: {{ option.delivery_time }} dias úteis
                            </small>
                          </div>
                        </div>
                      </template>
                    </v-radio>
                  </v-radio-group>


                  <v-card-actions class="justify-end mt-2">
                    <v-btn color="primary" :disabled="!selectedDelivery" @click="saveAddress">
                      Continuar
                    </v-btn>
                  </v-card-actions>
                </div>

              </div>
            </v-timeline-item>

            <!-- ETAPA 3: Pagamento -->
            <v-timeline-item :color="currentStep === 3 ? 'purple' : 'grey'">
              <template #icon>
                <v-icon :color="currentStep === 3 ? 'purple' : 'grey'">mdi-credit-card-outline</v-icon>
              </template>

              <template #opposite>
                <div v-if="currentStep === 3">
                  <v-card>
                    <v-toolbar>
                      <v-toolbar-title>Pagamento</v-toolbar-title>
                    </v-toolbar>

                    <v-card-text>
                      <v-tabs v-model="tab">
                        <v-tab value="credit">Crédito</v-tab>
                        <v-tab value="debit">Débito</v-tab>
                        <v-tab value="pix">Pix</v-tab>
                      </v-tabs>

                      <div v-if="tab === 'credit'">
                        <v-text-field label="Número do Cartão (Crédito)" />
                        Restante dos campos
                      </div>

                      <div v-else-if="tab === 'debit'">
                        <v-text-field label="Número do Cartão (Débito)" />
                        Restante dos campos
                      </div>

                      <div v-else-if="tab === 'pix'">
                     <!--   <v-text-field label="Chave Pix" /> -->
                        QrCode + Chave copia e cola
                      </div>

                    </v-card-text>
                  </v-card>

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
import addressForm from '@/address/addressForm.vue';


const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

const address = ref(null);
const route = useRoute()
const cartData = route.query.item ? JSON.parse(route.query.item) : { items: [] }
const coupons = ref([]);
const selectedCoupon = ref(null);
const appliedCoupon = ref(null);
const useTextInput = ref(false)
const couponText = ref('')
const addressFormRef = ref(null);
const availableDeliveries = ref([]);
const selectedDelivery = ref(null);
const tab = ref('credit');
const credit = ref(null);
const debit = ref(null);
const pix = ref(null);

// 👇 Faz o Vue reagir a mudanças no carrinho
const cart = reactive(cartData)

const currentStep = ref(1)

const nextStep = async () => {
  if (currentStep.value === 2) {
    let cep = null

    if (addressFormRef.value) {
      // formulário existe → pegar CEP do form
      const form = addressFormRef.value
      const isValid = await form.validate()
      if (!isValid) {
        alert('Preencha todos os campos obrigatórios corretamente.')
        return
      }
      cep = form.address.cep.replace(/\D/g, '')
    } else if (address.value) {
      // usar endereço já salvo
      cep = address.value.cep.replace(/\D/g, '')
    } else {
      alert('Nenhum endereço disponível.')
      return
    }

    const zipcodeOrigin = '97010002' // CEP da loja

    try {
      const products = JSON.parse(localStorage.getItem('cartProducts')) || []

      const { data } = await api.post('/melhorEnvio/calculate-delivery', {
        zipcode_origin: zipcodeOrigin,
        zipcode_destiny: cep,
        products
      })

      availableDeliveries.value = data
      console.log('Fretes calculados:', data)
    } catch (error) {
      console.error('Erro ao calcular frete:', error)
      alert('Erro ao calcular o frete. Tente novamente.')
      return
    }
  }

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

    if (!response.data || response.data.length === 0) {
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
  } catch (e) {
    console.log("Erro ao carregar cupons, tente novamente mais tarde", e);
  }
}

const applyCoupon = async () => {
  if (useTextInput.value) {
    if (!couponText.value) return

    try {
      // Chamada para verificar se o cupom existe
      const response = await api.get(`/coupon/validate-coupon/${couponText.value}`)

      if (!response.data || response.data.length === 0) {
        alert(`O cupom "${couponText.value}" não existe!`)
        return
      }

      const coupon = response.data[0] // assumindo que retorna array de cupons

      // Verifica se está expirado
      const now = new Date()
      const endDate = new Date(coupon.end_date)
      if (endDate < now) {
        alert(`O cupom "${coupon.title}" já expirou em ${formatDate(coupon.end_date)}!`)
        return
      }

      // Cupom válido
      appliedCoupon.value = coupon
      alert(`Cupom "${coupon.title}" aplicado com sucesso! Desconto: ${coupon.discount}%`)
      couponText.value = ''

    } catch (err) {
      console.error('Erro ao validar cupom:', err)
      alert('Erro ao validar o cupom. Tente novamente mais tarde.')
    }

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
    alert(`Cupom "${selectedCoupon.value.displayText}" aplicado com sucesso!`)
    selectedCoupon.value = null
  }
};
const calculateDelivery = async () => {
  let cep = null

  if (addressFormRef.value) {
    // formulário existe → pegar CEP do form
    const form = addressFormRef.value
    const isValid = await form.validate()
    if (!isValid) {
      alert('Preencha todos os campos obrigatórios corretamente.')
      return
    }
    cep = form.address.cep.replace(/\D/g, '')
  } else if (address.value) {
    // usar endereço já salvo
    cep = address.value.cep.replace(/\D/g, '')
  } else {
    alert('Nenhum endereço disponível.')
    return
  }

  const zipcodeOrigin = '97010002' // CEP da loja

  try {
    const products = JSON.parse(localStorage.getItem('cartProducts')) || []

    const { data } = await api.post('/melhorEnvio/calculate-delivery', {
      zipcode_origin: zipcodeOrigin,
      zipcode_destiny: cep,
      products
    })

    availableDeliveries.value = data
    console.log('Fretes calculados:', data)

  } catch (error) {
    console.error('Erro ao calcular frete:', error)
    alert('Erro ao calcular o frete.')
  }
};

const loadAddress = async () => {
  try {
    const response = await api.get('/address/get-address', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token") || localStorage.getItem('token')}`
      }
    });
    address.value = response.data[0];
  }
  catch (e) {
    console.log('nenhum endereço encontrado...');
  }
};

const saveAddress = async () => {
  try {
    let addressData = null

    if (addressFormRef.value) {
      // Formulário existe → valida e pega os dados
      const isValid = await addressFormRef.value.validate()
      if (!isValid) {
        alert('Por favor, preencha corretamente o endereço antes de continuar.')
        return
      }
      addressData = addressFormRef.value.address
    } else if (address.value) {
      // Formulário não existe → pegar endereço já salvo
      addressData = address.value
    } else {
      alert('Nenhum endereço disponível.')
      return
    }

    const data = {
      cep: addressData.cep,
      logradouro: addressData.logradouro,
      numero: addressData.numero,
      complemento: addressData.complemento,
      bairro: addressData.bairro,
      cidade: addressData.cidade,
      estado: addressData.estado,
      pais: addressData.pais,
      referencia: addressData.referencia,
      delivery_option: selectedDelivery?.company?.name || null,
      delivery_price: selectedDelivery?.price || null
    }

    console.log('Dados que serão enviados:', data)

    const response = await api.post('/address/create-address', data, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('token')}`
      }
    })

    // Atualiza endereço local
    address.value = { ...data, id: response.data.address_id }

    console.log('Endereço salvo com sucesso:', response.data)
    nextStep()
  } catch (e) {
    console.error('Erro ao salvar o endereço:', e)
    alert('Não foi possível salvar o endereço. Tente novamente.')
  }
};

onMounted(async () => {
  await getCoupon();
  await loadAddress();
});
</script>