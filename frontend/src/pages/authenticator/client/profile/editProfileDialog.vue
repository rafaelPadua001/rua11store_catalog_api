<template>
    <v-row>
        <v-col>
            <v-card>
                <v-card-title>
                    <h1>Edit profile user</h1>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text style="max-height: 500px; overflow-y: auto;">
                    <v-form ref="form" v-model="valid">
                        <v-row justify="center">
                            <v-col cols="12">
                                <h3>Personal</h3>
                            </v-col>
                            <v-divider></v-divider>

                            <v-col cols="3" class="d-flex flex-column justify-center">
                                <div class="avatar-wrapper position-relative d-inline-block">
                                    <!-- Avatar -->
                                    <v-avatar size="150" class="mt-4 overflow-hidden">
                                        <v-img :src="avatarPreview || defaultAvatar"></v-img>
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
                            <!--<v-col cols="12">
                                <!-- Avatar URL 
                                <v-file-input v-model="formData.avatar_file" label="Avatar" accept="image/*"
                                    prepend-icon="mdi-camera" placeholder="Select an image" @change="onAvatarChange" />
                            </v-col> -->
                        </v-row>
                        <v-row>
                            <v-col cols="6">

                                <!-- Name -->
                                <v-text-field v-model="formData.full_name" label="Name"
                                    :rules="[v => !!v || 'Name is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <!-- Email -->
                                <v-text-field v-model="formData.email" label="Email"
                                    :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                                    required></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12">
                                <h3>Address</h3>
                            </v-col>
                            <v-divider></v-divider>
                            <v-col cols="6">
                                <v-text-field v-model="formData.zip" label="ZIP / Postal Code"
                                    @blur="getAddressByZipCode()" :rules="[rules.required, rules.cep]"></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.street" label="Street / Address"
                                    :rules="[v => !!v || 'Street is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.complement" label="complement"
                                    :rules="[v => !!v || 'Complement is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.neighborhood" label="neighborhood"
                                    :rules="[v => !!v || 'Street is required']" required></v-text-field>
                            </v-col>

                            <v-col cols="4">
                                <v-text-field v-model="formData.city" label="City"
                                    :rules="[v => !!v || 'City is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.state" label="State"></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.country" label="Country"></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12">
                                <h3>Contact</h3>
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
import { ref, watch, reactive } from 'vue'
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

//const userId = localStorage.getItem('user_id');
const token = localStorage.getItem('access_token') || localStorage.getItem('token')

// Copia os dados do profile para formData
const formData = reactive({
    full_name: '',
    email: '',
    avatar_file: null,
    address: {
        street: '',
        city: '',
        state: '',
        zip: '',
        neighborhood: '',
        complement: '',
        country: ''
    },
    phone: '',
    mobile: ''
})

watch(
    () => props.profile,
    (newVal) => {
        formData.full_name = newVal.full_name || ''
        formData.email = newVal.email || ''
        formData.avatar_file = newVal.avatar_file || ''
        formData.address.street = newVal.address?.street || ''
        formData.address.city = newVal.address?.city || ''
        formData.address.state = newVal.address?.state || ''
        formData.address.zip = newVal.address?.zip || ''
        formData.address.country = newVal.address?.country || ''
        formData.address.complement = newVal.address?.complement || ''
        formData.address.neighborhood = newVal.address?.neighborhood || ''
        formData.phone = newVal.phone || ''
        formData.mobile = newVal.mobile || ''
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
        })
        formData.full_name = response.data.name;
        formData.email = response.data.email;
    }
    catch (e) {
        console.log('usuario não authenticado...');
    }
}

const onAvatarChange = () => {
    if (formData.avatar_file) {
        const file = formData.avatar_file
        avatarPreview.value = URL.createObjectURL(file)
    } else {
        avatarPreview.value = ''
    }
};

const rules = {
    required: value => !!value || 'Campo obrigatório',
    cep: value => /^\d{5}-\d{3}$/.test(value) || 'CEP inválido'
};

const getAddressByZipCode = async () => {
    const cleanCep = formData.zip.replace(/\D/g, '')
    if (cleanCep.length !== 8) return

    loadingCep.value = true
    try {
        const res = await fetch(`https://viacep.com.br/ws/${cleanCep}/json/`)
        const data = await res.json()

        if (!data.erro) {
            formData.street = data.logradouro || ''
            formData.neighborhood = data.bairro || ''
            formData.city = data.localidade || ''
            formData.state = data.uf || ''
            formData.complement = data.complemento || ''
            formData.country = data.country || ''

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
    let cep = formData.zip.replace(/\D/g, '')
    if (cep.length > 5) {
        cep = cep.substring(0, 5) + '-' + cep.substring(5, 8)
    }
    formData.zip = cep
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



watch(() => formData.zip, (newVal) => {
    if (newVal && newVal.length <= 9) formatZipcode()
});

const saveProfile = () => {
    if (form.value.validate()) {
        // Emite evento para o componente pai atualizar o perfil
        emit('update-profile', { ...formData })
        closeDialog()
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