<template>
  <v-row justify="center" no-gutters>
    <v-col class="d-flex flex-column">
       <v-form ref="addressForm">
    <v-row>
      <!-- CEP -->
      <v-col cols="12" md="8">
        <v-text-field v-model="address.cep" label="CEP" variant="outlined" @blur="fecthZipcode" :loading="loadingCep"
          maxlength="9" placeholder="00000-000" :rules="[rules.required, rules.cep]"></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <!-- Logradouro -->
      <v-col cols="12" md="8">
        <v-text-field v-model="address.logradouro" label="Logradouro" variant="outlined"
          :rules="[rules.required]"></v-text-field>
      </v-col>

      <!-- Número -->
     
    </v-row>
    <v-row>
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
      <v-col cols="12">
        <v-text-field v-model="address.referencia" label="Ponto de referência" variant="outlined"
          placeholder="Próximo a..."></v-text-field>
      </v-col>
    </v-row>
  </v-form>
    </v-col>
  </v-row>
 
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const estados = [
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
  'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
];

const address = reactive({
  cep: '',
  logradouro: '',
  numero: '',
  complemento: '',
  bairro: '',
  cidade: '',
  estado: '',
  pais: 'Brasil',
  referencia: ''
});

const loadingCep = ref(false);
const addressForm = ref(null);

const rules = {
  required: value => !!value || 'campo obrigatório',
  cep: value => /^\d{5}-\d{3}$/.test(value) || 'CEP inválido'
};

const fecthZipcode = async () => {
  const cleanCep = address.cep.replace(/\D/g, '');

  if (cleanCep.length !== 8) {
    return;
  }

  loadingCep.value = true;

  try {
    const response = await fetch(`https://viacep.com.br/ws/${cleanCep}/json/`);
    const data = await response.json();

    if (!data.erro) {
      // Preenche os campos com os dados da API
      address.logradouro = data.logradouro || '';
      address.bairro = data.bairro || '';
      address.cidade = data.localidade || '';
      address.estado = data.uf || '';
      address.complemento = data.complemento || '';
    }
    else {
      alert('CEP não encontrado');
    }
  }
  catch (e) {
    console.log('erro ao buscar CEP.', e);
    alert('ERRP ao buscar CEP. Tente novamente.');
  }
  finally {
    loadingCep.value = false;
  }
}

const formatZipcode = () => {
  let cep = address.cep.replace(/\D/g, '');

  if (cep.length > 5) {
    cep = cep.substring(0, 5) + '-' + cep.substring(5, 8);
  }

  address.cep = cep;
}

const validateAdrress = async () => {
  const { valid } = await addressForm.value.validate();

  if (valid) {
    nexStep();
  }
  else {
    alert('Preencha todos os campos obrigatórios corretamente');
  }
};

watch(() => address.cep, (newVal) => {
  if (newVal && newVal.length <= 9) {
    formatZipcode();
  }
});
</script>