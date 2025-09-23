<template>
  <v-container>
    <v-app-bar color="purple-darken-3" density="comfortable" flat>
      <!-- Nav icon à esquerda -->
      <v-app-bar-nav-icon @click="drawer = !drawer" v-if="isAuthenticated" />

      <!-- Logo + Texto juntos à esquerda -->
      <div class="d-flex align-center ml-0">
        <template v-if="logoUrl">
          <v-img :src="logoUrl" alt="Logo" width="60" height="60" contain class="mr-0" style="cursor: pointer"
            @click="$router.push('/')" />
        </template>
        <span v-else class="mr-2">Rua11Store</span>

        <v-divider :thickness="2" class="border-opacity-1 mx-2" inset vertical color="white"></v-divider>



      </div>
      <!-- Texto Blog -->
      <router-link :to="`/menagementPage/pageView/${pages.id}`">
        <span class="text-white">{{ pages.title }}</span>
      </router-link>
      <!-- Empurra qualquer outro conteúdo para a direita -->
      <v-spacer></v-spacer>



      <v-menu offset-y :nudge-y="20" content-class="custom-menu">
        <template #activator="{ props }">
          <v-btn icon v-bind="props" @click="showNotifications">
            <v-icon size="18">mdi-bell</v-icon>
            <div v-if="hasNewNotifications" class="red-dot"></div>
          </v-btn>
        </template>


        <v-list>
          <v-list-item v-for="(notification, index) in notifications" :key="index">
            <v-list-item-title>
              <v-card @click="markAsRead(notification.id)">
                <v-card-text>{{ notification.message }}</v-card-text>
                <v-card-actions>
                  <!-- <v-btn text @click="notification.show = true">Ver</v-btn> -->
                  <v-btn text @click="markAsRead(notification.id)">Marcar</v-btn>
                  <!-- <v-btn text @click="notification.show = false">Fechar</v-btn> -->

                </v-card-actions>
              </v-card>
            </v-list-item-title>
          </v-list-item>
          <v-list-item v-if="notifications.length === 0">
            <v-list-item-title class="text-grey">Sem notificações</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-snackbar v-model="snackbar.show" :timeout="5000" color="success">
        {{ snackbar.text }}
      </v-snackbar>
      <v-btn icon @click="navigateTo('/')">
        <v-icon size="18">mdi-domain</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" class="bg-purple-darken-3" theme="dark" temporary>
      <v-list dense>
        <v-list-item>
          <v-list-item-title class="text-h8">Menu</v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>

        <div v-if="isAuthenticated">
          <v-list-item link @click="navigateTo('/authenticator/dashboard')" prepend-icon="mdi-home"
            title="Dashboard"></v-list-item>
          <v-list-item link @click="navigateTo('/menagementPage/pages')" prepend-icon="mdi-file-document"
            title="Pages"></v-list-item>
          <v-list-item-group>

            <v-list-item>
              <template #prepend>
                <v-icon>mdi-post</v-icon>
              </template>
              <v-list-item-title @click="blogMenuOpen = !blogMenuOpen">Blogs</v-list-item-title>
            </v-list-item>

            <!-- Submenus -->
            <v-slide-y-transition>
              <div v-if="blogMenuOpen">
                <v-list-item link @click="navigateTo('/blog/blogs')" title="Articles" class="ps-12"></v-list-item>
                <v-list-item link @click="navigateTo('/blog/blogView/comments')" class="ps-12">
                  <v-list-item-title>Comentários</v-list-item-title>
                </v-list-item>
                <v-list-item link @click="navigateTo('/blog/comentarios-reportados')" class="ps-12">
                  <v-list-item-title>Comentários Reportados</v-list-item-title>
                </v-list-item>
              </div>
            </v-slide-y-transition>
          </v-list-item-group>



          <v-list-item link @click="navigateTo('/seo/seo')" prepend-icon="mdi-web" title="SEO"></v-list-item>
          <v-list-item link @click="navigateTo('/categories/categories')" prepend-icon="mdi-inbox"
            title="Categories"></v-list-item>
          <v-list-item link @click="navigateTo('/products/products')" prepend-icon="mdi-cart"
            title="Products"></v-list-item>
          <v-list-item link @click="navigateTo('/stock/stock')" prepend-icon="mdi-finance" title="Stock"></v-list-item>
          <v-list-item link @click="navigateTo('/payments/payments')" prepend-icon="mdi-wallet"
            title="Payments"></v-list-item>
          <v-list-item link @click="navigateTo('/delivery/delivery')" prepend-icon="mdi-moped"
            title="Delivery"></v-list-item>
          <v-list-item link @click="navigateTo('/orders/orders')" prepend-icon="mdi-package"
            title="Orders"></v-list-item>
          <v-list-item link @click="navigateTo('/coupons/coupons')" prepend-icon="mdi-bookmark"
            title="Coupons"></v-list-item>
          <v-list-item link @click="navigateTo('/comments/comment')" prepend-icon="mdi-comment-multiple"
            title="Comments"></v-list-item>
          <v-list-item link @click="navigateTo('/authenticator/profile')" prepend-icon="mdi-account"
            title="Profile"></v-list-item>
          <v-list-item link @click="logout" prepend-icon="mdi-logout" title="Logout"></v-list-item>
        </div>

        <div v-else>
          <v-list-item link @click="navigateTo('/')" prepend-icon="mdi-home" title="Home"></v-list-item>
          <v-list-item link @click="navigateTo('/authenticator/login')" prepend-icon="mdi-login"
            title="Login"></v-list-item>
        </div>
      </v-list>
    </v-navigation-drawer>




  </v-container>


</template>

<script setup>
import { ref, inject, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});



const logoUrl = ref('');
const drawer = ref(false);
const router = useRouter();
const isAuthenticated = ref(false);
const notifications = inject('notifications', ref([]));
const hasNewNotifications = inject('hasNewNotifications', ref(true));
const blogMenuOpen = ref(false);
let pages = inject('pages', ref([]));

const snackbar = ref({
  show: false,
  text: '',
});


const checkAuth = () => {
  isAuthenticated.value = !!localStorage.getItem('access_token');
  if (!isAuthenticated.value) {
    localStorage.removeItem('user_id');
  } else {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      const token = localStorage.getItem('access_token');
      const payload = parseJwt(token);
      if (payload && payload.user_id) {
        localStorage.setItem('user_id', payload.user_id);
      }
    }
  }
};

// Função para extrair user_id do JWT, caso não esteja salvo no localStorage
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

onMounted(async () => {
  getPages();
  try {
    const res = await api.get('/config/config');
    logoUrl.value = res.data.logo_url;
  }
  catch (error) {
    console.error("Erro ao carregar logo:", error);
  }
  checkAuth();
  window.addEventListener('storage', checkAuth);

});

onUnmounted(() => {
  window.removeEventListener('storage', checkAuth);

});

const showNotifications = () => {
  hasNewNotifications.value = false;
  fetchNotifications();

};

const navigateTo = (path) => {
  drawer.value = false;
  router.push(path);
};


const fetchNotifications = async () => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    console.warn("Usuário não autenticado, não é possível buscar notificações.");
    return;
  }

  // Pega user_id do localStorage ou extrai do token JWT
  let userId = localStorage.getItem('user_id');
  if (!userId) {
    const payload = parseJwt(token);
    userId = payload?.user_id || payload?.sub || null;
    if (userId) {
      localStorage.setItem('user_id', userId);
    }
  }

  if (!userId) {
    console.warn("User ID não encontrado, não é possível buscar notificações.");
    return;
  }

  try {
    const response = await api.get(`/notifications/notifications/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      params: {
        order_by: 'created_at',
        order: 'asc',  // ou 'desc'
      },
    });


    const fetched = response.data.notifications || response.data;

    // Só adiciona notificações novas para evitar duplicatas
    const existingMessages = notifications.value.map(n => n.message);

    fetched.forEach(n => {
      if (!existingMessages.includes(n.message)) {
        notifications.value.push({ id: n.id, message: n.message, show: false });
      }
    });
  } catch (error) {
    console.error('Erro ao buscar notificações:', error.response?.data || error.message);
  }
}

const markAsRead = async (notificationId) => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    console.warn("Usuário não autenticado, não é possível marcar notificações como lidas.");
    return;
  }

  try {
    await api.post(`/notifications/notifications/read/${notificationId}`, {}, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    // Encontra e remove a notificação do array
    const index = notifications.value.findIndex(n => n.id === notificationId);
    if (index !== -1) {
      snackbar.value.text = 'Notificação marcada como lida com sucesso!';
      snackbar.value.show = true;
      notifications.value.splice(index, 1); // remove do array
    }
  } catch (error) {
    console.error('Erro ao marcar notificação como lida:', error.response?.data || error.message);
    snackbar.value.text = 'Erro ao marcar notificação como lida.';
    snackbar.value.show = true;
  }
};

const getPages = async () => {

  try {
    const response = await api.get("/pages/pages/Blog");

    pages = response.data;

  } catch (error) {
    console.error("Error loading pages:", error);
  }
};

const logout = async () => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    alert("Você já está deslogado.");
    navigateTo('/authenticator/login');
    return;
  }

  try {
    const response = await axios.post(
      'https://rua11store-catalog-api-lbp7.onrender.com/auth/logout',
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.status === 200) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      window.dispatchEvent(new Event('storage'));
      alert('Logout realizado com sucesso!');
      navigateTo('/authenticator/login');
    }
  } catch (error) {
    console.error('Erro no logout:', error.response?.data || error.message);

    if (error.response?.status === 401 || error.response?.status === 422) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      window.dispatchEvent(new Event('storage'));
    }

    navigateTo('/authenticator/login');
  }
};
</script>

<style scoped>
.custom-menu {
  margin-top: 10px !important;
  /* Ajusta a distância vertical */
  max-height: 400px;
  /* Limita altura para facilitar scroll, se precisar */
}

.red-dot {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 10px;
  height: 10px;
  background-color: red;
  border-radius: 50%;
  z-index: 10;
}
</style>
