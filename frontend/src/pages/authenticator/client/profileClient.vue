<template>
  <v-container class="py-6">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-row justify="center" v-if="loading">

          <v-col cols="auto">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          </v-col>
        </v-row>
        <v-card class="pa-6" elevation="2" rounded="xl" v-else>

          <!-- Cabeçalho do perfil -->
          <v-row align="center" class="mb-6">
            <v-col cols="12" md="4" class="d-flex justify-center">
              <v-avatar size="120" v-if="profile.avatar_url">
                <v-img :src="`${profile.avatar_url}`" alt="User Avatar"></v-img>
              </v-avatar>
              <v-avatar size="120" v-else>
                <v-img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="User Avatar"></v-img>
              </v-avatar>
            </v-col>
            <v-col cols="12" md="8" class="text-center text-md-left">
              <h2 class="font-weight-bold mb-1" v-if="profile.full_name">{{ profile.full_name }}</h2>
              <h2 class="font-weight-bold mb-1" v-else>Marcos Obrien</h2>
              <!-- <p class="text-medium-emphasis mb-1">Network Engineer</p> -->
              <p class="text-caption" v-if="profile.username"><strong>Username:</strong> {{ profile.username }}</p>
              <p class="text-caption" v-else>marcos.obrien@example.com</p>
              <p class="text-caption" v-if="profile.email"><strong>Email:</strong> {{ profile.email }}</p>
              <p class="text-caption" v-else>marcos.obrien@example.com</p>
              <v-btn color="primary" variant="flat" size="small" class="mt-2" @click="openEditProfileDialog()">
                Edit Profile
              </v-btn>
            </v-col>
          </v-row>

          <v-divider class="mb-4"></v-divider>

          <!-- Bio 
          <h3 class="text-subtitle-1 font-weight-medium mb-2">About</h3>
          <p class="text-body-2 mb-6">
            Passionate network engineer with 8 years of experience in data
            security and infrastructure management. Loves technology,
            photography, and exploring new coffee places.
          </p>-->

          <!-- Informações extras -->
          <v-row dense>
            <v-col cols="12" sm="6">
              <v-card class="pa-3" variant="outlined" rounded="lg">
                <v-icon class="mr-2" color="blue">mdi-map-marker</v-icon>
                <span v-if="profile.addresses && profile.addresses.length">
                  {{ profile.addresses[0].city }}, {{ profile.addresses[0].state }}, {{ profile.addresses[0].country }}
                </span>
                <span v-else>
                  São Paulo, SP, Brazil
                </span>

              </v-card>
            </v-col>
            <v-col cols="12" sm="6">
              <v-card class="pa-3" variant="outlined" rounded="lg">
                <v-icon class="mr-2" color="green">mdi-calendar</v-icon>
                <span v-if="profile.created_at">Joined: {{ formatDateBr(profile.created_at) }}</span>
                <span v-else>Joined: March 2022</span>
              </v-card>
            </v-col>
          </v-row>

          <!-- Sessão inferior: pedidos, atividades, etc -->
          <h3 class="text-subtitle-1 font-weight-medium mt-6 mb-3">
            Recent Activity
          </h3>
          <v-divider></v-divider>

          <v-list density="compact" lines="two">
            <v-list-item prepend-icon="mdi-cart" title="Order #1024" subtitle="Placed 3 days ago"></v-list-item>
            <v-list-item prepend-icon="mdi-message" title="Commented on 'Network Setup Guide'"
              subtitle="2 days ago"></v-list-item>
            <v-list-item prepend-icon="mdi-account-edit" title="Updated profile info"
              :subtitle="formatDateBr(profile.updated_at)"></v-list-item>
          </v-list>

          <v-card-actions class="justify-center">
            <v-btn color="error" @click="removeAccount(profile.user_id)">
              Delete account
            </v-btn>
          </v-card-actions>
        </v-card>

        <v-dialog v-model="editDialog" width="800">
          <edit-profile-dialog v-model="editDialog" :profile="profile" @update-profile="handleUpdateProfile"
            @update:modelValue="val => editDialog = val" />
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import editProfileDialog from './profile/editProfileDialog.vue';

const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

const userId = localStorage.getItem('user_id');
const token = localStorage.getItem('access_token') || localStorage.getItem('token');
const profile = ref({});
const loading = ref(true);
const editDialog = ref(false);
let updatedProfile = ref([]);
let file = '';

const getProfileUser = async () => {
  try {
    const response = await api.get(`/profile/get-profile/${userId}`);
    profile.value = response.data;
  }
  catch (e) {
    console.log('Erro ao buscar perfil de usuário:', e);
  }
  finally {
    loading.value = false;
  }
};

const openEditProfileDialog = async () => {
  try {
    editDialog.value = true;
  }
  catch (e) {
    console.log('Erro ao abrir dialog', e);
  }
};

const handleUpdateProfile = async (updatedProfile) => {
  profile.value = { ...updatedProfile }
  console.log('Perfil Atualizado:', updatedProfile);

  try {
    const payload = new FormData();

    // Adiciona campos do perfil
    for (const key in updatedProfile) {

      if (key === "addresses") {
        // Converte endereço para JSON string
        payload.append(key, JSON.stringify(updatedProfile[key]));
        console.log(payload);
      } else if (key === "avatar_file") {
        // Não adiciona avatar_file aqui se vier separado
        continue;
      } else {
        payload.append(key, updatedProfile[key]);
      }
    }

    // Adiciona arquivo de avatar separadamente
    if (updatedProfile.avatar_file) {
      payload.append("avatar_file", updatedProfile.avatar_file); // Corrigido: usar payload em vez de formData
    }

    const response = await api.put(`/profile/update-profile/${userId}`, payload, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });

    profile.value = response.data;
  }
  catch (e) {
    console.log("Erro ao atualizar dados de usuario", e);
  }
}

const formatDateBr = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
};

const removeAccount = async (userId) => {
  if(!confirm('Tem certeza que deseja remover sua conta permanentemente ?')) return;
  try{
    const response = await api.delete(`/profile/delete-profile/${userId}`);
    if(response.status === 200 || response.status === 204){
      profile.value = null;
      alert('Conta removida com sucesso !');
      window.location.href = '/authenticator/client/clientLogin';
      logout();
    }
    else {
      console.error('Erro inesperado ao remover conta:', response);
      alert('Erro inesperado ao remover a conta.');
    }
  }
  catch(e){
    console.log('Erro ao remover a sua conta, tente novamente.', e);
    alert('Erro ao remover a sua conta, tente novamente.');
  }
  
};

const logout = async () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
  const payload = JSON.parse(atob(token.split('.')[1]));
  const user_type = payload.user_type;

  if (!token && user_type === 'client') {
    alert("Você já está deslogado.");
    navigateTo('/authenticator/client/clientLogin');
    return;
  }

  try {
    const response = await api.post(
      '/client/logoutClient',
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.status === 200) {
      localStorage.removeItem('access_token') || localStorage.removeItem('token');
      localStorage.removeItem('user_id');
      window.dispatchEvent(new Event('storage'));
      alert('Logout realizado com sucesso!');

      if (user_type !== 'client') {
        return navigateTo('/authenticator/Login');
      }
      else {
        return navigateTo('/authenticator/client/clientLogin');
      }

      // navigateTo('/authenticator/client/clientLogin');
    }
  } catch (error) {
    console.error('Erro no logout:', error.response?.data || error.message);

    if (error.response?.status === 401 || error.response?.status === 422) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      window.dispatchEvent(new Event('storage'));
    }

    navigateTo('/authenticator/client/clientLogin');
  }
};

onMounted(() => {
  getProfileUser();
});
</script>