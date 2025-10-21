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
                                <!-- Preview do avatar -->
                                <v-avatar size="150" class="mt-4">
                                    <v-img :src="avatarPreview || defaultAvatar"></v-img>
                                </v-avatar>
                            </v-col>
                            <v-col cols="12">
                                <!-- Avatar URL -->
                                <v-file-input v-model="formData.avatar_file" label="Avatar" accept="image/*"
                                    prepend-icon="mdi-camera" placeholder="Select an image" @change="onAvatarChange" />
                            </v-col>
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
                                <v-text-field v-model="formData.street" label="Street / Address"
                                    :rules="[v => !!v || 'Street is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-text-field v-model="formData.city" label="City"
                                    :rules="[v => !!v || 'City is required']" required></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.state" label="State"></v-text-field>
                            </v-col>
                            <v-col cols="4">
                                <v-text-field v-model="formData.zip" label="ZIP / Postal Code"></v-text-field>
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
                                    :rules="[v => !!v || 'Phone is required']" required></v-text-field>
                            </v-col>

                            <v-col cols="6">
                                <v-text-field v-model="formData.mobile" label="Mobile"
                                    :rules="[v => !!v || 'Mobile is required']" required></v-text-field>
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

const props = defineProps({
    modelValue: { type: Boolean, required: true },
    profile: { type: Object, required: true }
})

const emit = defineEmits(['update:modelValue', 'update-profile'])

const defaultAvatar = 'https://cdn.vuetifyjs.com/images/john.jpg'
const valid = ref(false)
const form = ref(null)
const avatarPreview = ref('')

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
        formData.phone = newVal.phone || ''
        formData.mobile = newVal.mobile || ''
    },
    { immediate: true }
)

const closeDialog = () => {
    emit('update:modelValue', false)
}

const onAvatarChange = () => {
    if (formData.avatar_file) {
        const file = formData.avatar_file
        avatarPreview.value = URL.createObjectURL(file)
    } else {
        avatarPreview.value = ''
    }
}

const saveProfile = () => {
    if (form.value.validate()) {
        // Emite evento para o componente pai atualizar o perfil
        emit('update-profile', { ...formData })
        closeDialog()
    }
}
</script>