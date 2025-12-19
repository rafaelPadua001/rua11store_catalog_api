<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="12">
        <v-card elevation="0">
          <v-card-text>
            <v-timeline :direction="timelineDirection" line-inset="12">
              <!-- ETAPA 1: Itens -->
              <v-timeline-item fill-dot :color="currentStep === 1 ? 'primary' : 'grey'" dot-color="deep-purple">
                <template v-slot:icon>
                  <v-icon :color="currentStep === 1 ? 'yellow' : 'grey'">mdi-cart-outline</v-icon>
                </template>

                <div v-if="currentStep === 1">
                  <v-row no-gutters>
                    <v-col cols="12" md="6">
                      <v-list>
                        <v-list-item v-for="(item, index) in cart.items" :key="index">
                          <v-card class="d-flex flex-column w-full max-w-lg mx-auto" elevation="0">

                            <v-avatar size="150">
                              <v-img :src="item.product_image" :alt="item.product_name" cover></v-img>
                            </v-avatar>
                            <v-row>
                              <v-col cols="12" sm="12" md="6">
                                <strong>{{ item.product_name }}</strong>
                              </v-col>
                              <v-spacer></v-spacer>
                              <v-col cols="12" sm="12" md="6">
                                <strong>R$ {{ item.product_price }}</strong>
                              </v-col>

                              <v-col cols="12" sm="12" md="6">
                                <strong>Variations:</strong>
                              </v-col>
                              <v-col cols="12" sm="12" md="6">
                                <div v-for="(variation, index) in item.variations" :key="index">
                                  <v-chip v-if="variation.variation_type === 'Size'">
                                    {{ variation.value }}
                                  </v-chip>
                                  <v-chip v-else :color="variation.value">

                                  </v-chip>
                                </div>

                              </v-col>
                              <v-spacer></v-spacer>

                              <v-col cols="12" sm="12" md="2">
                                <strong>Qtd:</strong>
                              </v-col>
                              <v-col cols="12" sm="12" md="4">
                                <v-text-field :model-value="getItemQuantity(item)"
                                  @update:model-value="val => setItemQuantity(item, val)" type="number" min="1"
                                  density="compact" hide-details style="width: 80px" @click.stop @mousedown.stop />

                              </v-col>
                              <v-col cols="12" sm="12" md="6">
                                <strong>R$ {{ (Number(getItemQuantity(item)) * Number(item.product_price)).toFixed(2)
                                }}</strong>
                              </v-col>
                            </v-row>
                            <v-card-actions>
                              <v-btn color="error" size="small" @click="removeItemCart(item)">Remover</v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-list-item>
                      </v-list>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-card class="w-100">
                        <v-card-title>
                          Resumo
                        </v-card-title>
                        <v-card-text>
                          <v-row>
                            <v-col cols="12" sm="12" md="6">
                              <strong>Subtotal em produtos:</strong>
                            </v-col>
                            <v-col cols="12" sm="12" md="6">
                              R$ {{ totalCarrinho.toFixed(2) }}
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col cols="12" sm="12" md="6">
                              <strong>Total com desconto (%):</strong>
                            </v-col>
                            <v-col v-if="appliedCoupon && appliedCoupon.discount">

                              R$ {{ (totalCarrinho - (totalCarrinho * appliedCoupon.discount / 100)).toFixed(2) }}
                            </v-col>

                          </v-row>
                          <v-row>
                            <v-col cols="12" sm="12" md="6">
                              <strong>Total:</strong>
                            </v-col>
                            <v-col cols="12" sm="12" md="6">
                              R$ {{
                                appliedCoupon && appliedCoupon.discount
                                  ? (totalCarrinho - (totalCarrinho * appliedCoupon.discount / 100)).toFixed(2)
                                  : totalCarrinho.toFixed(2)
                              }}
                            </v-col>
                          </v-row>


                          <v-row>
                            <v-col cols="12" sm="12" md="10">

                              <!-- Alterna entre select e input -->
                              <div class="d-flex flex-wrap align-center gap-2">
                                <div class="flex-grow-1 min-w-0">
                                  <v-select v-if="!useTextInput" v-model="selectedCoupon" :items="formattedCoupons"
                                    item-title="displayText" item-value="id" label="Selecione um cupom" outlined dense
                                    :menu-props="{ maxHeight: '300px' }" return-object></v-select>

                                  <v-text-field v-else v-model="couponText" label="Digite o cupom" outlined
                                    dense></v-text-field>
                                </div>

                                <!-- Botão para alternar -->
                                <v-btn text class="ms-1" variant="tonal" @click="useTextInput = !useTextInput">
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

                          <v-row justify="center" class="mt-0">
                            <v-col cols="12" sm="12" md="6">
                              <v-btn color="success" @click="applyCoupon" :disabled="!selectedCoupon && !couponText">
                                Aplicar cupom
                              </v-btn>
                            </v-col>
                          </v-row>

                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                          <v-row justify="end">
                            <v-col cols="auto">
                              <!-- <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>-->
                              <v-btn color="primary" @click="nextStep">Avançar</v-btn>
                            </v-col>
                          </v-row>
                        </v-card-actions>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
              </v-timeline-item>

              <!-- ETAPA 2: Endereço -->
              <v-timeline-item :color="currentStep === 2 ? 'success' : 'grey'" dot-color="deep-purple" fill-dot>
                <template v-slot:icon>
                  <v-icon :color="currentStep === 2 ? 'yellow' : 'grey'">mdi-truck-outline</v-icon>
                </template>


                <div v-if="currentStep === 2" class="d-flex flex-column w-full max-w-lg mx-auto">
                  <v-row justify="center">
                    <v-col cols="12" md="12">
                      <addressForm ref="addressFormRef" v-if="!address" />
                      <v-card v-else>
                        <v-toolbar color="deep-purple-accent-4">
                          <v-toolbar-title>
                            <v-icon>mdi-map-marker</v-icon>
                            Endereço de Entrega</v-toolbar-title>
                        </v-toolbar>
                        <v-divider></v-divider>
                        <v-card-text>
                          <v-row>
                            <v-col>
                              <v-col cols="12" sm="8"><strong>CEP:</strong> {{ address.cep }}</v-col>
                              <v-col cols="12" sm="12"><strong>Logradouro:</strong> {{ address.logradouro }}</v-col>
                              <v-col cols="12" sm="12"><strong>Número:</strong> {{ address.numero }}</v-col>
                              <v-col cols="12" sm="12" v-if="address.complemento"><strong>Complemento:</strong> {{
                                address.complemento
                              }}</v-col>
                              <v-col cols="12" sm="12"><strong>Bairro:</strong> {{ address.bairro }}</v-col>
                              <v-col cols="12" sm="12"><strong>Cidade:</strong> {{ address.cidade }}</v-col>
                              <v-col cols="12" sm="12"><strong>Estado:</strong> {{ address.estado }}</v-col>
                              <v-col cols="12" sm="12"><strong>País:</strong> {{ address.pais }}</v-col>
                              <v-col cols="12" v-if="address.referencia"><strong>Referência:</strong> {{
                                address.referencia }}</v-col>
                            </v-col>
                          </v-row>

                        </v-card-text>

                        <v-card-actions>
                          <v-btn @click="openAddressDialog(address)">Editar</v-btn>
                          <v-btn @click="removeAddress(address)">Remover</v-btn>
                        </v-card-actions>
                      </v-card>
                      <v-card-actions class="justify-space-between mt-2" v-if="!availableDeliveries.length">
                        <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                        <v-btn color="primary" @click="calculateDelivery">Calcular Frete</v-btn>
                      </v-card-actions>
                    </v-col>
                  </v-row>


                  <div v-if="availableDeliveries.length" class="mt-4">
                    <h4 class="mb-1">Opções de entrega</h4>

                    <v-radio-group v-model="selectedDelivery" class="pa-2">
                      <template v-for="(option, index) in availableDeliveries" :key="index">
                        <v-radio :value="option" class="my-2" v-if="option && !option.error">

                          <template #label>

                            <div class="d-flex align-center gap-3">
                              <!-- Logo -->
                              <v-img v-if="option.company && option.company.picture" :src="option.company.picture"
                                alt="Logo {{ option.company.name }}" max-width="50" max-height="30" cover
                                class="rounded-sm"></v-img>
                              <v-icon v-else color="grey" size="30">mdi-truck-delivery-outline</v-icon>
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
                      </template>
                    </v-radio-group>


                    <v-card-actions class="justify-end mt-0">
                      <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                      <v-btn color="primary" :disabled="!selectedDelivery" @click="saveAddress()">
                        Continuar
                      </v-btn>
                    </v-card-actions>
                  </div>

                </div>
              </v-timeline-item>

              <!-- ETAPA 3: Pagamento -->
              <v-timeline-item :color="currentStep === 3 ? 'purple' : 'grey'" fill-dot dot-color="deep-purple">
                <template v-slot:icon>
                  <v-icon :color="currentStep === 3 ? 'yellow' : 'grey'">
                    mdi-credit-card-outline
                  </v-icon>
                </template>

                <!-- ❌ Removemos o #opposite porque ele está cortando o card -->
                <!-- <template #opposite>
    <span class="text-h8">Pagamento</span>
  </template> -->

                <div v-if="currentStep === 3" class="timeline-content d-flex flex-column">

                  <v-card class="d-flex flex-column w-full max-w-lg mx-auto" elevation="2" rounded="lg">
                    <v-toolbar flat>
                      <v-toolbar-title class="text-h6">Pagamento</v-toolbar-title>
                    </v-toolbar>

                    <v-card-text class="pt-2">
                      <v-row dense>
                        <v-col cols="12" md="6">
                          <strong>Frete:</strong> R${{ selectedDelivery.price }}
                        </v-col>
                        <v-col cols="12" md="6">
                          <strong>Subtotal:</strong> R${{ Number(totalCarrinho).toFixed(2) }}
                        </v-col>
                      </v-row>

                      <v-row justify="center">
                        <v-col cols="12" class="text-center">
                          <span class="text-h6 font-weight-bold">
                            Total: R$
                            {{
                              (
                                (Number(selectedDelivery.price) + Number(totalCarrinho)) /
                                payment.installments
                              ).toFixed(2)
                            }}
                          </span>
                        </v-col>
                      </v-row>

                      <v-divider class="my-2"></v-divider>

                      <v-tabs v-model="tab" color="primary" fixed-tabs>
                        <v-tab value="credit">Crédito</v-tab>
                        <v-tab value="debit">Débito</v-tab>
                        <v-tab value="pix">Pix</v-tab>
                      </v-tabs>

                      <div class="mt-0">
                        <!-- Campos compartilhados -->
                        <div v-if="tab === 'credit' || tab === 'debit'">
                          <v-select v-model="payment.payment_method_id" :items="cardBrands" label="Bandeira do Cartão"
                            item-value="id" item-title="name" variant="underlined" density="comfortable" />

                          <VMaskInput
                            :label="tab === 'credit' ? 'Número do Cartão (Crédito)' : 'Número do Cartão (Débito)'"
                            v-model="payment.card_number" mask="credit-card" variant="underlined" />

                          <v-text-field label="Nome do Titular" v-model="payment.name" variant="underlined" />
                          <VMaskInput label="CPF" v-model="payment.cpf" mask="###.###.###-##" variant="underlined" />
                          <v-text-field label="Email" v-model="payment.email" :rules="[
                            v => !!v || 'E-mail é obrigatório',
                            v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'E-mail inválido',
                          ]" variant="underlined" />
                          <v-text-field label="Código de Segurança" v-model="payment.security_code" maxlength="3"
                            variant="outlined"
                            @input="payment.security_code = payment.security_code.replace(/\\D/g, '')" />
                          <v-text-field v-model="payment.expiration_date" label="Validade (MM/YYYY)" maxlength="7"
                            placeholder="MM/YYYY" @input="formatExpiration" variant="underlined" />

                          <v-select v-if="tab === 'credit'" label="Parcelas"
                            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]" v-model="payment.installments"
                            variant="underlined" />
                        </div>

                        <div v-else-if="tab === 'pix'" class="text-center">
                          <v-img :src="qrCodeImg" max-width="200" class="mx-auto my-4" />
                          <v-text-field label="Chave Pix (copia e cola)" v-model="payment.pix_key" />
                          <v-text-field label="Nome" v-model="payment.name" />
                          <v-text-field label="CPF" v-model="payment.cpf" />
                          <v-text-field label="Email" v-model="payment.email" />
                        </div>
                      </div>
                    </v-card-text>

                    <v-card-actions class="justify-space-around pt-0">
                      <v-btn color="primary" @click="prevStep" size="small">Voltar</v-btn>
                      <v-btn color="success" @click="submitPayment" size="small">
                        Finalizar Pedido
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </div>
              </v-timeline-item>

            </v-timeline>
          </v-card-text>
        </v-card>

        <v-dialog v-model="addressDialog" max-width="600">
          <v-card class="w-full max-w-md">
            <v-card-title>Editar Endereço</v-card-title>
            <v-card-text>
              <addressForm v-if="addressDialog" :address="address" :editing="true" @updated="onUpdated"
                @cancel="addressDialog = false" ref="addressFormRef" />
            </v-card-text>

          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>

</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import addressForm from '@/address/addressForm.vue';
import { useDisplay } from 'vuetify'
import PaymentResult from './payment_result.vue';
import { SHA256 } from 'crypto-js';


const { mdAndUp } = useDisplay()

const timelineDirection = computed(() => (mdAndUp.value ? 'horizontal' : 'vertical'))
const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

const token = localStorage.getItem('access_token') || localStorage.getItem('token');
const userId = localStorage.getItem('user_id');
let profileUser = ref([]);

const address = ref(null);
const addressDialog = ref(false);
const route = useRoute()
const cartData = JSON.parse(sessionStorage.getItem('checkout_item') || '{"items": []}');
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
const payment = ref({
  card_number: '',
  name: '',
  cpf: '',
  email: '',
  security_code: '',
  expiration_date: '',
  pix_key: '',
  coupon_code: '',
  coupon_amount: 0,
  total_value: 0,
  installments: 1,
  payment_method_id: null,
});
const paymentStatus = ref(null);
const paymentMessage = ref('');

const cardBrands = [
  { id: 'visa', name: 'Visa' },
  { id: 'mastercard', name: 'Mastercard' },
  { id: 'elo', name: 'Elo' },
  { id: 'amex', name: 'American Express' },
  { id: 'hipercard', name: 'Hipercard' },
  { id: 'cabal', name: 'Cabal' },
];

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

    const zipcodeOrigin = '73082180' // CEP da loja

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

const getItemQuantity = (item) => {

  if (item.variations?.length) {
    return item.variations.reduce(
      (t, v) => t + (v.quantity || 0),
      0
    )
  }
  return item.quantity || 0
}

const setItemQuantity = (item, value) => {
  const qty = Number(value) || 0

  if (item.variations?.length) {
    item.variations.forEach(v => {
      v.quantity = qty
    })
  } else {
    item.quantity = qty
  }
}


const totalCarrinho = computed(() => {
  if (!Array.isArray(cart.items)) return 0

  return cart.items.reduce((acc, item) => {
    const price = Number(item.product_price) || 0

    const quantity = item.variations?.length
      ? item.variations.reduce(
          (t, v) => t + (Number(v.quantity) || 0),
          0
        )
      : Number(item.quantity) || 0

    return acc + price * quantity
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
      // console.log('Você não possui cupom');
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

const loadProfile = async () => {
  try {
    const response = await api.get(`/profile/get-profile/${userId}`);
    profileUser = response.data;
    console.log(profileUser);
  }
  catch (e) {
    console.log("erro ao carregar perfil do usuario", e);
  }
};

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

  const zipcodeOrigin = '97010002'
  try {
    const products = (cart.items || []).map(item => ({
      product_id: item.product_id,
      quantity: item.quantity,
      product_weight: Number(item.product_weight || 0),
      product_height: Number(item.product_height || 0),
      product_width: Number(item.product_width || 0),
      product_length: Number(item.product_length || 0)
    }));

    // console.log(cart.items);

    const { data } = await api.post('/melhorEnvio/calculate-delivery', {
      zipcode_origin: zipcodeOrigin,
      zipcode_destiny: cep,
      products
    });

    const companyLogos = {
      1: 'https://static.melhorenvio.com.br/logo/correios.png',
      6: 'https://static.melhorenvio.com.br/logo/latam-cargo.png',
      9: 'https://static.melhorenvio.com.br/logo/azul-cargo.png',
      12: 'https://static.melhorenvio.com.br/logo/buslog.png'
    };


    const validDeliveries = Array.isArray(data)
      ? data
        .filter(d => !d?.error && Number(d?.price) > 0)
        .map(d => ({
          ...d,
          company: {
            ...d.company,
            picture: companyLogos[d.company?.id] || null
          }
        }))
      : []

    availableDeliveries.value = validDeliveries

    if (validDeliveries.length === 0) {
      alert('Nenhuma transportadora disponível para esse endereço.');
    }
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
      delivery_price: selectedDelivery?.price || null,

    }

    const response = await api.post('/address/create-address', data, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    // Atualiza endereço local
    address.value = { ...data, user_id: userId, id: response.data.address_id }

    nextStep()
  } catch (e) {
    console.error('Erro ao salvar o endereço:', e)
    alert('Não foi possível salvar o endereço. Tente novamente.')
  }
};

const openAddressDialog = (address) => {
  addressDialog.value = true;
}

const onUpdated = async (updatedAddress) => {
  try {
    address.value = { ...updatedAddress, id: address.value.id }

    addressDialog.value = false

    const token = localStorage.getItem('access_token') || localStorage.getItem('token');

    const response = await api.put(`/address/update-address/${address.value.id}`, address.value, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  catch (e) {
    console.log('Erro ao atualizar endereço.', e);
  }

};

const removeAddress = async (addr) => {
  if (!confirm('Deseja realmente remover este endereço?')) return;

  try {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    await api.delete(`/address/delete-address/${addr.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Limpa o endereço
    address.value = null;
    if (addressFormRef.value) {
      addressFormRef.value.resetForm?.();
    }
    //   console.log('Endereço removido');
  } catch (e) {
    console.log('Não foi possível remover endereço', e);
  }
};



const removeItemCart = async (item) => {
  console.log(item);
  try {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    const response = await api.delete(`/cart/cart-item-remove/${item.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 200 && response.data.message == "Item removido com sucesso.") {
      cart.items = cart.items.filter(i => i.id !== item.id)
      //console.log('Item removido');
    }
  }
  catch (e) {
    console.log('Erro ao remover item. Tente novamente...', e);
  }
}


function formatExpiration() {
  let val = payment.value.expiration_date.replace(/\D/g, ''); // só números

  if (val.length > 6) val = val.slice(0, 6); // limita a MMYYYY

  if (val.length <= 2) {
    payment.value.expiration_date = val; // só mês digitado
  } else {
    payment.value.expiration_date = val.slice(0, 2) + '/' + val.slice(2); // adiciona '/' automaticamente
  }
}
async function submitPayment() {
  try {
    console.log('🚀 Iniciando processo de pagamento...');

    const deliveryPrice = parseFloat(selectedDelivery?.value.price || 0);

    const cartTotal = parseFloat(totalCarrinho?.value || 0);
    const totalAmount = deliveryPrice + cartTotal;

    const payload = {
      paymentType: tab.value,
      total: totalAmount,
      coupon_code: payment.value.coupon_code || null,
      coupon_amount: payment.value.coupon_amount || 0,
      name: payment.value.name,
      recipient_name: profileUser.full_name,
      cpf: payment.value.cpf,
      email: payment.value.email,
      userId: userId,
      products: cartData.items,
      address: address.value,
    };


    if (tab.value === 'credit' || tab.value === 'debit') {
      const [monthStr, yearStr] = payment.value.expiration_date.split('/');

      const expiration_month = parseInt(monthStr, 10);
      const expiration_year = parseInt(yearStr, 10);

      if (isNaN(expiration_month) || isNaN(expiration_year)) {
        paymentStatus.value = 'rejected';
        paymentMessage.value = 'Data de expiração inválida';
        return;
      }

      payload.card_data = {
        card_number: payment.value.card_number.replace(/\s/g, ''),
        expiration_month,
        expiration_year,
        security_code: payment.value.security_code
      };

      payload.installments = payment.value.installments;
      payload.payment_method_id = payment.value.payment_method_id || 'visa';
      console.log(payment.value.payment_method_id);

    }
    //  console.log('📤 Enviando para backend:', payload);

    // ⚡ ENVIA PARA SEU BACKEND PYTHON
    const response = await api.post('/payment/payment', payload);
    console.log('✅ Resposta do backend:', response.data);

    if (response.data.status === 'approved') {
      paymentStatus.value = 'approved';
      paymentMessage.value = 'Pagamento aprovado com sucesso!';
      localStorage.setItem('paymentStatus', paymentStatus.value);
      localStorage.setItem('paymentMessage', paymentMessage.value);
      const eventId = crypto.randomUUID();

      fbq('track', 'Purchase', {
        content_ids: [order.id],
        value: order.total,
        currency: 'BRL',
        contents: cart.value.map(i => ({
          id: i.id,
          quantity: i.quantity,
          item_price: i.price
        })),
        content_type: 'product',
        eventId: eventId
      });

      //Send to meta conversion
      await sendMetaConversion(totalAmount, cart, payment, eventId);

      window.location.href = `/payments/client/payment_result?status=${paymentStatus}&message=${paymentMessage}`;

    } else if (response.data.status === 'pending') {
      paymentStatus.value = 'pending';
      paymentMessage.value = 'Pagamento pendente. Aguarde confirmação.';
      window.location.href = `/payments/client/payment_result?status=${paymentStatus}&message=${paymentMessage}`;

    } else if (response.data.status === 'rejected') {
      paymentStatus.value = 'rejected';
      paymentMessage.value = response.data.message || 'Pagamento rejeitado.';
      window.location.href = `/payments/client/payment_result?status=${paymentStatus}&message=${paymentMessage}`;

    } else {
      paymentStatus.value = 'rejected';
      paymentMessage.value = response.data.message || 'Pagamento rejeitado.';
      window.location.href = `/payments/client/payment_result?status=${paymentStatus}&message=${paymentMessage}`;
    }

  } catch (error) {
    paymentStatus.value = 'rejected';
    paymentMessage.value = 'Erro desconhecido. Tente novamente.';
    console.log('Erro desconhecido. Tente novamente.', error);
    window.location.href = `/payments/client/payment_result?status=${paymentStatus}&message=${paymentMessage}`;

  }
}

async function sendMetaConversion(totalAmount, cart, payment, eventId) {
  try {
    await api.post('/meta/meta/conversion', {
      event_name: 'Purchase',
      event_id: eventId,
      value: totalAmount,
      contents: cart.value.map(item => ({
        id: item.id,
        quantity: item.quantity,
        item_price: item.price,
      })),
      email_hash: sha256(payment.value.email?.trim().toLowerCase() || ''),
      phone_hash: sha256(payment.value.phone?.replace(/\D/g, '') || ''),
      event_source_url: window.location.href
    });

    console.log('Conversion enviada ao backend (CAPI)');
  }
  catch (e) {
    console.log("Erro ao enviar Conversion API:", error);
  }
}

onMounted(async () => {
  await getCoupon();
  await loadProfile();
  await loadAddress();
  await calculateDelivery();
  const totalReal =
    totalCarrinho.value;

  if (typeof window.fbq === "function") {
    window.fbq("track", "InitiateCheckout", {
      content_ids: cart.value?.map(item => item.id) ?? [],
      value: totalReal ?? 0,
      currency: "BRL"
    });
  }
  try {
    mp.value = new MercadoPago('APP_USR-f969c2eb-5d4f-4e5c-974d-ace6053a80a8', {
      locale: 'pt-BR'
    });
    //  console.log('✅ MercadoPago inicializado:', mp.value);
  } catch (error) {
    // console.log('❌ Erro ao inicializar MercadoPago:', error);
  }
});
</script>
