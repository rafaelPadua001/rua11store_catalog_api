<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="6">
        <v-card class="pa-4">
          <v-card-title>Perfil do Usuário</v-card-title>
          <v-spacer></v-spacer>
          <v-divider></v-divider>
          
         
          <!-- Contêiner para o avatar e o botão de upload -->
          <v-row class="d-flex align-center justify-center">
            <v-col cols="auto" class="d-flex justify-center">
              <!-- Avatar com ícone de upload dentro -->
              <v-avatar size="100" class="mx-auto" style="position: relative; display: flex; justify-content: center;">
                
                <v-img
                  :src="user && user.avatar_url ? user.avatar_url : 'https://imgs.search.brave.com/Zsapxs7JqY0v8BYpGwgMnI1WLK_J9l-O1IMIOUuzTGc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9waWNz/LmNyYWl5b24uY29t/LzIwMjQtMDktMDcv/djc1XzNnV0VUTWVL/UHJmWmFXWlFKQS53/ZWJw'"
                  alt="Avatar" class="rounded-circle" style="object-fit: cover;" />

                <!-- Ícone de upload dentro da imagem -->
                <v-icon @click="triggerFileInput" class="upload-icon" size="24" color="white"
                  style="position: absolute; bottom: 5px; right: 5px; cursor: pointer; background: rgba(0, 0, 0, 0.5); border-radius: 50%; padding: 5px;">
                  mdi-pencil
                </v-icon>
              </v-avatar>
            </v-col>

            <!-- Input escondido para o upload -->
            <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="uploadAvatar" />
          </v-row>

          <!-- Informações do perfil -->
          <v-card-text v-if="user">
            <p><strong>Nome:</strong> {{ user.name }}</p>
            <p><strong>Usuário:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Data de Nascimento:</strong> ({{ calculateAge(user.birth_date) }} anos)</p>
          </v-card-text>


          <v-card-text v-else>
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </v-card-text>

          <v-card-actions class="pt-0 d-flex justify-center">
            <v-btn color="primary" text="edit" variant="text">Edit</v-btn>
          </v-card-actions>

        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

const user = ref(null);
const fileInput = ref(null);

// Função para buscar o perfil do usuário
const fetchUserProfile = async () => {
  const token = localStorage.getItem('access_token');
  console.log("Token armazenado:", token); // Verificando o token armazenado

  if (!token) {
    console.error('Nenhum token encontrado. Faça login novamente.');
    return false;
  }

  try {
    const response = await api.get('/auth/profile', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    user.value = response.data; // Atualiza os dados do usuário com a resposta
    console.log("Dados do usuário:", user.value); // Verificando os dados do usuário
  } catch (error) {
    console.error('Erro ao buscar o perfil do usuário:', error.response?.data || error.message);
  }
};

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
  else {
    console.log("Elemento de input não encontrado");
  }
}


// Função para calcular a idade a partir da data de nascimento
const calculateAge = (birthDate) => {
  const birthDateObj = new Date(birthDate);
  const today = new Date();
  let age = today.getFullYear() - birthDateObj.getFullYear();
  const monthDifference = today.getMonth() - birthDateObj.getMonth();

  // Ajuste se o aniversário ainda não ocorreu este ano
  if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDateObj.getDate())) {
    age--;
  }

  return age;
};

// Função para formatar a data para exibição
const formatDate = (dateString) => {
  if (!dateString) return "Não informado";
  return new Date(dateString).toLocaleDateString('pt-BR'); // Formata a data no formato brasileiro
};

// Função para fazer upload do avatar
const uploadAvatar = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('avatar', file);

  const token = localStorage.getItem('access_token');

  if (!token) {
    console.error('Nenhum token encontrado. Faça login novamente.');
    return;
  }

  try {
    const response = await api.post('/auth/upload-avatar', formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });

    // Atualizar a URL do avatar após o upload
    user.value.avatar_url = response.data.avatar_url;
    console.log('Avatar atualizado:', response.data.avatar_url);
  } catch (error) {
    console.error('Erro ao atualizar o avatar:', error.response?.data || error.message);
  }
};

// Chama a função de busca de dados ao montar o componente
onMounted(fetchUserProfile);
</script>

<style scoped>
.upload-icon {
  position: absolute;
  bottom: 5px;
  right: 5px;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  padding: 5px;
}
</style>
