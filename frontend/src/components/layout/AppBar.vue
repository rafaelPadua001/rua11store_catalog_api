<template>
  <v-app-bar color="purple-darken-3" density="comfortable">
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    <v-app-bar-title>Rua11Store</v-app-bar-title>

    <v-spacer></v-spacer>
    <v-btn icon @click="goToHome">
      <v-icon>mdi-domain</v-icon>
    </v-btn>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" temporary>
    <v-list>
      <v-list-item>
        <v-list-item-title class="text-h6">Menu</v-list-item-title>
      </v-list-item>

      <v-divider></v-divider>
      <div v-if="isAuthenticated">
        <v-list-item link @click="goToDashboard" prepend-icon="mdi-home" title="Dashboard"></v-list-item>
        <v-list-item link @click="goToCategories" prepend-icon="mdi-inbox" title="Categories"></v-list-item>
        <v-list-item link @click="goToProducts" prepend-icon="mdi-cart" title="Products"></v-list-item>
        <v-list-item link @click="goToStock" prepend-icon="mdi-package" title="Stock"></v-list-item>
        <v-list-item link @click="goToPayments" prepend-icon="mdi-wallet" title="Payments"></v-list-item>
        <v-list-item link @click="goToProfile" prepend-icon="mdi-account" title="Profile"></v-list-item>
        <v-list-item link @click="logout" prepend-icon="mdi-logout" title="Logout"></v-list-item>
      </div>

      <div v-else>
        <v-list-item link @click="goToHome" prepend-icon="mdi-home" title="Home"></v-list-item>
        <v-list-item link @click="goToLogin" prepend-icon="mdi-login" title="Login"></v-list-item>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from "axios";

const drawer = ref(false);
const router = useRouter();
const isAuthenticated = ref(false);

// Verifica autenticação ao carregar e quando o token muda
const checkAuth = () => {
  isAuthenticated.value = !!localStorage.getItem('user_token');
};

onMounted(() => {
  checkAuth();
  window.addEventListener("storage", checkAuth);
});

const goToHome = () => {
  drawer.value = false;
  router.push('/');
};

const goToDashboard = () => {
  drawer.value = false;
  router.push('/authenticator/dashboard');
};

const goToCategories = () => {
  drawer.value = false;
  router.push('/categories/categories')
}

const goToLogin = () => {
  drawer.value = false;
  router.push('/authenticator/login');
};

const goToProducts = () => {
  drawer.value = false;
  router.push('/products/products')
};

const goToStock = () => {
  drawer.value = false;
  router.push('/stock/stock')
}

const goToPayments = () => {
  drawer.value = false;
  router.push('/payments/payments')
}

const goToProfile = async () => {
  drawer.value = false;
  router.push('/authenticator/profile')
}

const logout = async () => {
  const token = localStorage.getItem('user_token');

  if (!token) {
    alert("Você já está deslogado.");
    router.push('/authenticator/login');
    return;
  }

  try {
    const response = await axios.post(
      'https://rua11storecatalogapi-production.up.railway.app/auth/logout',
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.status === 200) {
      localStorage.removeItem('user_token');
      window.dispatchEvent(new Event("storage")); // Dispara evento para atualizar `isAuthenticated`
      alert('Logout realizado com sucesso!');
      router.push('/authenticator/login');
    }
  } catch (error) {
    console.error('Erro no logout:', error.response?.data || error.message);

    if (error.response?.status === 401 || error.response?.status === 422) {
      localStorage.removeItem('user_token');
      window.dispatchEvent(new Event("storage"));
    }

    router.push('/authenticator/login');
  }
};

</script>