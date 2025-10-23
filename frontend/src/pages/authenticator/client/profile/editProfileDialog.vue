<template>
    <v-row>
        <v-col>
            <v-card>
                <v-card-title>
                    <span class="text-h5">Edit profile user</span>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text style="max-height: 500px; overflow-y: auto;">
                    <v-form ref="form" v-model="valid">
                        <v-row justify="center">
                            <v-col cols="12">
                                <span class="text-subtitle text-h6">Personal</span>
                            </v-col>
                            <v-divider></v-divider>

                            <v-col cols="auto" class="d-flex flex-column justify-center">
                                <div class="avatar-wrapper position-relative d-inline-block">
                                    <!-- Avatar -->
                                    <v-avatar class="mt-4 overflow-hidden" size="150">
                                        <v-img :src="avatarPreview || profile.avatar_url || defaultAvatar" :alt="profile.avatar_url"></v-img>
                                    </v-avatar>


                                    <!-- Fundo escurecido com blur -->
                                    <div class="avatar-overlay"></div>

                                    <!-- Botão sobre a imagem -->
                                    <v-btn icon="mdi-camera" class="avatar-upload-btn"
                                        @click="$refs.fileInput.click()"></v-btn>

                                    <!-- Input oculto -->
                                    <v-file-input v-model="formData.avatar_file" ref="fileInput" type="file"
                                        accept="image/*" class="d-none" @change="onAvatarChange" />
                                </div>
                            </v-col>
                        </v-row>
                        <v-row dense justify-sm="center">
                            <v-col cols="6">
                                <!-- Name -->
                                <v-text-field v-model="formData.full_name" label="Name"
                                    :rules="[v => !!v || 'Name is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <!-- Username -->
                                <v-text-field v-model="formData.user_name" label="Username"
                                    :rules="[v => !!v || 'Name is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <!-- Email -->
                                <v-text-field v-model="formData.email" label="Email"
                                    :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                                    required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.birth_date" label="Birth Date" type="date"
                                    :rules="[v => !!v || 'Birth date is required']" required></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12">
                                <span class="text-subtitle text-h6">Address</span>
                            </v-col>
                            <v-divider></v-divider>
                            <v-col cols="6">
                                <v-text-field v-model="formData.addresses.zip" label="ZIP / Postal Code"
                                    @blur="getAddressByZipCode()" :rules="[rules.required, rules.cep]"></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.addresses.street" label="Street / Address"
                                    :rules="[v => !!v || 'Street is required']" required></v-text-field>
                            </v-col>
                            <!-- ADICIONE ESTE CAMPO AQUI -->
                            <v-col cols="6">
                                <v-text-field v-model="formData.addresses.number" label="Number"
                                    :rules="[v => !!v || 'Number is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.addresses.complement" label="Complement"></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.addresses.neighborhood" label="Neighborhood"
                                    :rules="[v => !!v || 'Neighborhood is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.addresses.city" label="City"
                                    :rules="[v => !!v || 'City is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.addresses.state" label="State"
                                    :rules="[v => !!v || 'State is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.addresses.country" label="Country"
                                    :rules="[v => !!v || 'Country is required']" required></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12">
                                <span class="text-subtitle text-h6">Contact</span>
                            </v-col>
                            <v-divider class="mb-4"></v-divider>
                            <v-col cols="6">
                                <v-text-field v-model="formData.phone" label="Phone"
                                    :rules="[v => !!v || 'Phone is required']" required prepend-inner-icon="mdi-phone"
                                    @input="formatPhoneInput('phone')"></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.mobile" label="Mobile"
                                    :rules="[v => !!v || 'Mobile is required']" required
                                    append-inner-icon="mdi-phone-plus"
                                    @input="formatPhoneInput('mobile')"></v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions class="justify-end">
                    <v-btn color="grey" @click="closeDialog">Cancel</v-btn>
                    <v-btn color="primary" @click="saveProfile">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, watch, reactive, onMounted } from 'vue' // Adicione onMounted aqui
import axios from 'axios'

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const props = defineProps({
    modelValue: { type: Boolean, required: true },
    profile: { type: Object, required: true }
})

const emit = defineEmits(['update:modelValue', 'update-profile'])

const defaultAvatar = 'https://cdn.vuetifyjs.com/images/john.jpg'
const valid = ref(false)
const form = ref(null)
const avatarPreview = ref('')
const loadingCep = ref(false)
const user = ref([])
const token = localStorage.getItem('access_token') || localStorage.getItem('token')

// Copia os dados do profile para formData
const formData = reactive({
    full_name: '',
    user_name: '',
    birth_date: '',
    email: '',
    avatar_file: null,
    addresses: {
        zip: '',
        street: '',
        number: '',
        complement: '',
        neighborhood: '',
        city: '',
        state: '',
        country: ''
      },
    phone: '',
    mobile: ''
})

watch(
    () => props.profile,
    (newVal) => {
        formData.full_name = newVal.full_name || ''
        formData.user_name = newVal.username
        formData.birth_date = newVal.birth_date || ''
        formData.email = newVal.email || ''
        formData.avatar_file = null
        if (newVal.avatar_file) {
            avatarPreview.value = newVal.avatar_file
        }
        formData.avatar_file = newVal.avatar_file
        formData.addresses.street = newVal.addresses?.street || ''
        formData.addresses.number = newVal.addresses?.number || newVal.address?.numero || '' // ADICIONE ESTA LINHA
        formData.addresses.city = newVal.addresses?.city || ''
        formData.addresses.state = newVal.addresses?.state || ''
        formData.addresses.zip = newVal.addresses?.zip || ''
        formData.addresses.country = newVal.addresses?.country || ''
        formData.addresses.complement = newVal.addresses?.complement || ''
        formData.addresses.neighborhood = newVal.addresses?.neighborhood || ''
        formData.phone = newVal.phone || ''
        formData.mobile = newVal.mobile || ''

        // Se tiver avatar_url, use para o preview
        if (newVal.avatar_url) {
            avatarPreview.value = newVal.avatar_url
        }
    },
    { immediate: true }
)

const closeDialog = () => {
    emit('update:modelValue', false)
};

const getAuthenticatedUser = async () => {
    try {
        const response = await api.get(`/client/get-logged-client`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        formData.full_name = response.data.name;
        formData.email = response.data.email;
        formData.user_name = response.data.profile.username;// se tiver username
        formData.birth_date = response.data.profile.birth_date;

        // Preenche os dados do endereço (o primeiro endereço, se houver)
        if (response.data.addresses && response.data.addresses.length > 0) {
            formData.addresses = {
                zip: response.data.addresses[0].zip || '',
                street: response.data.addresses[0].street || '',
                number: response.data.addresses[0].number || '',
                complement: response.data.addresses[0].complement || '',
                neighborhood: response.data.addresses[0].neighborhood || '',
                city: response.data.addresses[0].city || '',
                state: response.data.addresses[0].state || '',
                country: response.data.addresses[0].country || '',
            };
        } else {
            formData.addresses = {
                zip: '',
                street: '',
                number: '',
                complement: '',
                neighborhood: '',
                city: '',
                state: '',
                country: '',
            };
        }

    } catch (e) {
        console.log('Usuário não autenticado...', e);
    }
};


const onAvatarChange = () => {
    const file = formData.avatar_file
    if (file) {
        avatarPreview.value = URL.createObjectURL(file)
    } else {
        avatarPreview.value = ''
    }
}


const rules = {
    required: value => !!value || 'Campo obrigatório',
    cep: value => /^\d{5}-\d{3}$/.test(value) || 'CEP inválido'
};

const getAddressByZipCode = async () => {
    const cleanCep = formData.addresses.zip.replace(/\D/g, '')
    if (cleanCep.length !== 8) return

    loadingCep.value = true
    try {
        const res = await fetch(`https://viacep.com.br/ws/${cleanCep}/json/`)
        const data = await res.json()

        if (!data.erro) {
            formData.addresses.street = data.logradouro || ''
            formData.addresses.neighborhood = data.bairro || ''
            formData.addresses.city = data.localidade || ''
            formData.addresses.state = data.uf || ''
            formData.addresses.complement = data.complemento || ''
            formData.addresses.number = data.number || ''
            // O campo "number" não é preenchido automaticamente pelo ViaCEP
            // pois o número é específico de cada endereço
        } else {
            alert('CEP não encontrado')
        }
    } catch (e) {
        console.error('Erro ao buscar CEP:', e)
        alert('Erro ao buscar CEP. Tente novamente.')
    } finally {
        loadingCep.value = false
    }
};

// Formatar CEP enquanto digita
const formatZipcode = () => {
    let cep = formData.addresses.zip.replace(/\D/g, '')
    if (cep.length > 5) {
        cep = cep.substring(0, 5) + '-' + cep.substring(5, 8)
    }
    formData.addresses.zip = cep
};

const formatPhoneInput = (field) => {
    let val = formData[field].replace(/\D/g, '')
    if (val.length > 10) {
        val = val.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3')
    } else if (val.length > 5) {
        val = val.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3')
    } else if (val.length > 2) {
        val = val.replace(/^(\d{2})(\d{0,5})/, '($1) $2')
    } else {
        val = val.replace(/^(\d*)/, '($1')
    }
    formData[field] = val
}

watch(() => formData.addresses.zip, (newVal) => {
    if (newVal && newVal.length <= 9) formatZipcode()
});

const saveProfile = () => {
    // Validação adicional para o campo number
    if (!formData.addresses.number || formData.addresses.number.trim() === '') {
        alert('Por favor, informe o número do endereço.')
        return
    }

    if (form.value.validate()) {
        console.log('Dados a serem enviados:', formData)
        // Emite evento para o componente pai atualizar o perfil
        emit('update-profile', { ...formData })
        emit('update:modelValue', false)
    }
}

onMounted(() => {
    getAuthenticatedUser();
});
</script>

<style scoped>
.avatar-wrapper {
    position: relative;
    display: inline-block;
    cursor: pointer;
}

.avatar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(2px);
    border-radius: 50%;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.avatar-upload-btn {
    position: absolute;
    bottom: 12px;
    right: 12px;
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: black !important;
    opacity: 0;
    transition: opacity 0.3s ease, transform 0.2s ease;
}

.avatar-wrapper:hover .avatar-overlay,
.avatar-wrapper:hover .avatar-upload-btn {
    opacity: 1;
}

.avatar-wrapper:hover .avatar-upload-btn {
    transform: scale(1.05);
}
</style>