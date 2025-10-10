<template>
  <v-row justify="center" no-gutters>
    <v-col class="d-flex flex-column">
      <v-form ref="addressForm">
        <v-row>
          <!-- CEP -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.cep" label="CEP" variant="outlined" @blur="fetchZipcode"
              :loading="loadingCep" maxlength="9" placeholder="00000-000"
              :rules="[rules.required, rules.cep]"></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <!-- Logradouro -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.logradouro" label="Logradouro" variant="outlined"
              :rules="[rules.required]"></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <!-- Número -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.numero" label="Número" variant="outlined"
              :rules="[rules.required]"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="address.complemento" label="Complemento" variant="outlined"
              placeholder="Apto, Bloco, Casa, etc."></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <!-- Bairro -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.bairro" label="Bairro" variant="outlined"
              :rules="[rules.required]"></v-text-field>
          </v-col>
          <!-- Cidade -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.cidade" label="Cidade" variant="outlined"
              :rules="[rules.required]"></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <!-- Estado -->
          <v-col cols="12" md="6">
            <v-select v-model="address.estado" :items="estados" label="Estado" variant="outlined"
              :rules="[rules.required]"></v-select>
          </v-col>
          <!-- País -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.pais" label="País" variant="outlined" value="Brasil" readonly></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <!-- Referência -->
          <v-col cols="12" md="6">
            <v-text-field v-model="address.referencia" label="Ponto de referência" variant="outlined"
              placeholder="Próximo a..."></v-text-field>
          </v-col>

        </v-row>
        <v-card-actions v-if="editing">
          <v-btn color="primary" @click="$emit('updated', { ...address })">Salvar</v-btn>
          <v-btn text @click="$emit('cancel')">Cancelar</v-btn>
        </v-card-actions>

      </v-form>
    </v-col>
  </v-row>


</template>

<script setup>
import { ref, reactive, watch, defineExpose } from 'vue'

const props = defineProps({
  address: {
    type: Object,
    default: () => ({})
  },
  editing: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['updated']);
const form = ref({ ...props.address });

watch(() => props.address, (newVal) => {
  form.value = { ...newVal }
}, { immediate: true });

const estados = [
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
  'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

const addressForm = ref(null)
const loadingCep = ref(false)

const address = reactive({
  cep: props.address?.cep || '',
  logradouro: props.address?.logradouro || '',
  numero: props.address?.numero || '',
  complemento: props.address?.complemento || '',
  bairro: props.address?.bairro || '',
  cidade: props.address?.cidade || '',
  estado: props.address?.estado || '',
  pais: props.address?.pais || 'Brasil',
  referencia: props.address?.referencia || ''
})

const rules = {
  required: value => !!value || 'Campo obrigatório',
  cep: value => /^\d{5}-\d{3}$/.test(value) || 'CEP inválido'
}

// Função de validação que o pai poderá chamar
const validate = async () => {
  if (!addressForm.value) return false
  return await addressForm.value.validate()
}

// Expor método e dados para o pai
defineExpose({
  validate,
  address
})

const fetchZipcode = async () => {
  const cleanCep = address.cep.replace(/\D/g, '')
  if (cleanCep.length !== 8) return

  loadingCep.value = true
  try {
    const res = await fetch(`https://viacep.com.br/ws/${cleanCep}/json/`)
    const data = await res.json()

    if (!data.erro) {
      address.logradouro = data.logradouro || ''
      address.bairro = data.bairro || ''
      address.cidade = data.localidade || ''
      address.estado = data.uf || ''
      address.complemento = data.complemento || ''
    } else {
      alert('CEP não encontrado')
    }
  } catch (e) {
    console.error('Erro ao buscar CEP:', e)
    alert('Erro ao buscar CEP. Tente novamente.')
  } finally {
    loadingCep.value = false
  }
}

// Formatar CEP enquanto digita
const formatZipcode = () => {
  let cep = address.cep.replace(/\D/g, '')
  if (cep.length > 5) {
    cep = cep.substring(0, 5) + '-' + cep.substring(5, 8)
  }
  address.cep = cep
}


watch(() => address.cep, (newVal) => {
  if (newVal && newVal.length <= 9) formatZipcode()
})
</script>
