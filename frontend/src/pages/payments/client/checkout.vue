<template>
  <v-row justify="center">
    <v-col cols="12" sm="12" md="10" lg="10" xl="6">
      <v-card class="pa-4" elevation="0">
        <v-card-text>
          <v-timeline :direction="timelineDirection" line-inset="12">
            <!-- ETAPA 1: Itens -->
            <v-timeline-item fill-dot :color="currentStep === 1 ? 'primary' : 'grey'" dot-color="deep-purple">
              <template #icon>
                <v-icon :color="currentStep === 1 ? 'yellow' : 'grey'">mdi-cart-outline</v-icon>
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
                          <v-card class="pa-2 mb-2 d-flex flex-column" elevation="0">
                            <v-avatar size="50">
                              <v-img :src="item.product_image" :alt="item.product_name" cover></v-img>
                            </v-avatar>
                            <v-row>
                              <v-col cols="12" md="6">
                                <strong>{{ item.product_name }}</strong>
                              </v-col>
                              <v-spacer></v-spacer>
                              <v-col cols="12" md="3">
                                <strong>R$ {{ item.product_price }}</strong>
                              </v-col>
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
                            <v-col cols="12" md="6">
                              <strong>Subtotal em produtos:</strong>
                            </v-col>
                            <v-col cols="12" md="6">
                              R$ {{ totalCarrinho.toFixed(2) }}
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col cols="12" md="6" s>
                              <strong>Total com desconto (%):</strong>
                            </v-col>
                            <v-col v-if="appliedCoupon && appliedCoupon.discount">

                              R$ {{ (totalCarrinho - (totalCarrinho * appliedCoupon.discount / 100)).toFixed(2) }}
                            </v-col>

                          </v-row>
                          <v-row>
                            <v-col cols="12" md="6">
                              <strong>Total:</strong>
                            </v-col>
                            <v-col cols="12" md="6">
                              R$ {{
                                appliedCoupon && appliedCoupon.discount
                                  ? (totalCarrinho - (totalCarrinho * appliedCoupon.discount / 100)).toFixed(2)
                                  : totalCarrinho.toFixed(2)
                              }}
                            </v-col>
                          </v-row>


                          <v-row>
                            <v-col cols="12" md="10">

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

                          <v-row justify="center" class="mt-2">
                            <v-col cols="12" md="6">
                              <v-btn color="success" @click="applyCoupon" :disabled="!selectedCoupon && !couponText">
                                Aplicar cupom
                              </v-btn>
                            </v-col>
                          </v-row>

                        </v-card-text>
                        <v-card-actions>
                          <v-row justify="end" class="mt-4">
                            <v-col cols="auto">
                              <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                              <v-btn color="primary" @click="nextStep">Avançar</v-btn>
                            </v-col>
                          </v-row>
                        </v-card-actions>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>


              </template>

              <h3>Checkout Items</h3>
            </v-timeline-item>

            <!-- ETAPA 2: Endereço -->
            <v-timeline-item :color="currentStep === 2 ? 'success' : 'grey'" dot-color="deep-purple">
              <template #icon>
                <v-icon :color="currentStep === 2 ? 'yellow' : 'grey'">mdi-truck-outline</v-icon>
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
                    <template v-for="(option, index) in availableDeliveries" :key="index">
                      <v-radio :value="option" class="my-2" v-if="option && !option.error" >
                      
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


                  <v-card-actions class="justify-end mt-2">
                    <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                    <v-btn color="primary" :disabled="!selectedDelivery" @click="saveAddress">
                      Continuar
                    </v-btn>
                  </v-card-actions>
                </div>

              </div>
            </v-timeline-item>

            <!-- ETAPA 3: Pagamento -->
            <v-timeline-item :color="currentStep === 3 ? 'purple' : 'grey'" dot-color="deep-purple">
              <template #icon>
                <v-icon :color="currentStep === 3 ? 'yellow' : 'grey'">mdi-credit-card-outline</v-icon>
              </template>

              <template #opposite>
                <div v-if="currentStep === 3">
                  <v-card>
                    <v-toolbar flat>
                      <v-toolbar-title>Pagamento</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text class="justify-center">
                      <div>
                        <v-row>
                          <v-col>
                            <span>shippment: R$ {{ selectedDelivery.price }}</span>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col>
                            <span>Subtotal: R${{ Number(totalCarrinho).toFixed(2) }}</span>
                          </v-col>
                        </v-row>
                        <v-row justify="center">
                          <v-col cols="auto">
                            <span class="text-h4 ">Total: R$ {{ (Number(selectedDelivery.price) +
                              Number(totalCarrinho)).toFixed(2) }}</span>
                          </v-col>
                        </v-row>

                      </div>

                    </v-card-text>

                    <v-card-text>
                      <v-tabs v-model="tab" background-color="primary" dark>
                        <v-tab value="credit">Crédito</v-tab>
                        <v-tab value="debit">Débito</v-tab>
                        <v-tab value="pix">Pix</v-tab>
                      </v-tabs>

                      <!-- Campos compartilhados -->
                      <div v-if="tab === 'credit' || tab === 'debit'">
                        <v-text-field
                          :label="tab === 'credit' ? 'Número do Cartão (Crédito)' : 'Número do Cartão (Débito)'"
                          v-model="payment.card_number" />
                        <v-text-field label="Nome do Titular" v-model="payment.name" />
                        <v-text-field label="CPF" v-model="payment.cpf" />
                        <v-text-field label="Email" v-model="payment.email" />
                        <v-text-field label="Código de Segurança" v-model="payment.security_code" />
                        <v-text-field label="Validade" v-model="payment.expiration_date" />

                        <!-- Select de parcelas só para crédito -->
                        <v-select v-if="tab === 'credit'" label="Parcelas"
                          :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]" v-model="payment.installments" outlined />
                      </div>


                      <div v-else-if="tab === 'pix'">
                        <v-img :src="qrCodeImg" max-width="200" />
                        <v-text-field label="Chave Pix (copia e cola)" v-model="payment.pix_key" />
                        <v-text-field label="Nome" v-model="payment.name" />
                        <v-text-field label="CPF" v-model="payment.cpf" />
                        <v-text-field label="Email" v-model="payment.email" />
                        <!-- <v-text-field label="Cupom" v-model="payment.coupon_code" />
                        <v-text-field label="Valor do Cupom" v-model="payment.coupon_amount" />
                        <v-text-field label="Total" v-model="payment.total_value" />-->
                      </div>
                    </v-card-text>

                    <v-card-actions class="justify-space-between mt-2">
                      <v-btn color="grey" variant="tonal" @click="prevStep">Voltar</v-btn>
                      <v-btn color="success" @click="submitPayment">Finalizar Pedido</v-btn>
                    </v-card-actions>
                  </v-card>
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
import { useDisplay } from 'vuetify'

const { mdAndUp } = useDisplay()

const timelineDirection = computed(() => (mdAndUp.value ? 'horizontal' : 'vertical'))
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
});


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
    const products = (cart.items || []).map(item => ({
      product_id: item.product_id,
      quantity: item.quantity,
      product_weight: Number(item.product_weight || 0),
      product_height: Number(item.product_height || 0),
      product_width: Number(item.product_width || 0),
      product_length: Number(item.product_length || 0)
    }));

    console.log(cart.items);

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

    if(validDeliveries.length === 0){
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

const createCardToken = async (cardData) => {
  if (!mp.value) {
    throw new Error('MercadoPago não foi inicializado');
  }

  const token = await mp.value.card.createToken({
    cardNumber: cardData.cardNumber,
    cardholderName: cardData.cardholderName,
    cardExpirationMonth: cardData.cardExpirationMonth,
    cardExpirationYear: cardData.cardExpirationYear,
    securityCode: cardData.securityCode,
    identificationType: cardData.identificationType,
    identificationNumber: cardData.identificationNumber
  });

  return token;
};

async function submitPayment() {
  try {
    console.log('🚀 Iniciando processo de pagamento...');

    const deliveryPrice = parseFloat(selectedDelivery?.price || 0);
    const cartTotal = parseFloat(totalCarrinho?.value || 0);
    const totalAmount = deliveryPrice + cartTotal;

    const payload = {
      paymentType: tab.value,
      total: totalAmount,
      coupon_code: payment.value.coupon_code || null,
      coupon_amount: payment.value.coupon_amount || 0,
      name: payment.value.name,
      cpf: payment.value.cpf,
      email: payment.value.email,
    };

    // ⚡ APENAS campos que você realmente tem disponível
    // Remova os que não existem no seu componente

    // Se você tem produtos no carrinho, adicione:
    // payload.products = itemsDoCarrinho.value || []

    // Se você tem endereço, adicione:
    // payload.address = enderecoSelecionado.value || {}

    if (tab.value === 'credit' || tab.value === 'debit') {
      const [month, year] = payment.value.expiration_date.split('/');

      // ⚡ ENVIA OS DADOS DO CARTÃO PARA O BACKEND CRIAR O TOKEN
      payload.card_data = {
        card_number: payment.value.card_number.replace(/\s/g, ''),
        expiration_month: month?.trim(),
        expiration_year: year?.trim(),
        security_code: payment.value.security_code
      };

      payload.installments = payment.value.installments;
      payload.payment_method_id = "visa" // ou detecte a bandeira
    }

    console.log('📤 Enviando para backend:', payload);

    // ⚡ ENVIA PARA SEU BACKEND PYTHON
    const response = await api.post('/payment/payment', payload);
    console.log('✅ Resposta do backend:', response.data);

    if (response.data.status === 201 || response.data.status === 'approved' || response.data.success) {
      alert('Pagamento processado com sucesso!');
    } else {
      alert('Erro no pagamento: ' + (response.data.message || 'Tente novamente'));
    }

  } catch (error) {
    console.error('❌ Erro detalhado:', error);
    alert('Erro ao processar pagamento: ' + error.message);
  }
}



onMounted(async () => {
  await getCoupon();
  await loadAddress();
  try {
    mp.value = new MercadoPago('APP_USR-f969c2eb-5d4f-4e5c-974d-ace6053a80a8', {
      locale: 'pt-BR'
    });
    console.log('✅ MercadoPago inicializado:', mp.value);
  } catch (error) {
    console.log('❌ Erro ao inicializar MercadoPago:', error);
  }
});
</script>