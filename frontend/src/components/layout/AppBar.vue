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
      <div v-if="!isAuthenticated && !isClient">
        <router-link to="/authenticator/client/clientLogin">
          <span class="text-white">
            <v-icon icon="mdi-login"></v-icon>
          </span>
        </router-link>

      </div>

      <div v-if="isAuthenticated">
        <v-menu offset-y :nudge-y="20" content-class="custom-menu">
          <template #activator="{ props }">
            <v-btn icon v-bind="props" @click="showCartItems">
              <v-icon>mdi-cart</v-icon>
            </v-btn>
          </template>
          <v-list :lines="false" max-width="400">
            <v-list-item>
              <v-list-item-title class="text-h6">Carrinho</v-list-item-title>
            </v-list-item>

            <v-divider></v-divider>

            <template v-if="cartItems.length">
              <!-- Itera pelos carrinhos -->
              <v-list-item v-for="(cart, index) in cartItems" :key="cart.id" class="py-2">
                <v-list-item-subtitle class="text-caption text-grey mb-2">
                  Criado em: {{ new Date(cart.created_at).toLocaleString() }}
                </v-list-item-subtitle>

                <!-- Itera pelos itens dentro de cada carrinho -->
                <v-card v-for="(item, i) in cart.items" :key="item.id" elevation="1"
                  class="mb-2 pa-2 d-flex align-center" width="350" style="gap: 12px;">

                  <v-avatar>
                    <v-img :src="item.product_image" width="60" height="60" contain class="rounded "></v-img>
                  </v-avatar>


                  <div class="flex-grow-2">
                    <div class="font-weight-medium">{{ item.product_name }}</div>

                    <div class="d-flex align-center flex-wrap" style="gap: 6px;">

                      <!-- Chips -->
                      <div v-for="(variation, index) in item.variations" :key="index">
                        <v-chip v-if="variation.variation_type === 'Size'" size="small">
                          {{ variation.value }}
                        </v-chip>

                        <v-chip v-else :color="variation.value" size="small">
                          {{ colorNames[variation.value?.toUpperCase()] || variation.value }}
                        </v-chip>
                      </div>

                      <!-- Textfield do lado -->
                      <v-text-field v-model.number="item.quantity" type="number" min="1" density="compact" hide-details
                        class="ml-2" style="max-width: 70px;" @click.stop @mousedown.stop></v-text-field>

                    </div>


                    <div class="text-caption text-grey">
                      {{ item.quantity }}x — R$ {{ item.product_price }}
                    </div>
                  </div>

                  <div>
                    <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                      @click.stop="removeItem(item)"></v-btn>
                  </div>
                </v-card>

                <v-divider class="my-2"></v-divider>

                <div class="d-flex justify-space-between align-center mt-2">
                  <strong>Total:</strong>
                  <span>
                    R$
                    {{
                      cart.items
                        .reduce((acc, i) => acc + i.product_price * i.quantity, 0).toFixed(2)

                    }}
                  </span>
                </div>

                <v-card-actions class="justify-center mt-2">
                  <v-btn color="primary" size="small" variant="tonal" @click="checkout(cart)"
                    :disabled="cart.items.length === 0">Finalizar Compra</v-btn>
                </v-card-actions>
              </v-list-item>
            </template>

            <v-list-item v-else>
              <v-list-item-title class="text-grey text-center">Nenhum item no carrinho</v-list-item-title>
            </v-list-item>
          </v-list>

        </v-menu>


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
      </div>



      <v-snackbar v-model="snackbar.show" :timeout="5000" color="success">
        {{ snackbar.text }}
      </v-snackbar>
      <!--<v-btn icon @click="navigateTo('/')">
        <v-icon size="18">mdi-domain</v-icon>
      </v-btn>-->
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" class="bg-purple-darken-3" theme="dark" temporary>
      <v-list dense>
        <v-list-item>
          <v-list-item-title class="text-h8">Menu</v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>

        <div v-if="isAuthenticated && !isClient">

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
                  <v-list-item-title>Comments</v-list-item-title>
                </v-list-item>
                <!--  <v-list-item link @click="navigateTo('/blog/comentarios-reportados')" class="ps-12">
                  <v-list-item-title>Comentários Reportados</v-list-item-title>
                </v-list-item>-->
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

        <!-- Client itens -->
        <div v-else-if="isAuthenticated && isClient">
          <v-list-item link @click="navigateTo('/authenticator/client/clientDashboard')" prepend-icon="mdi-home"
            title="Dashboard"></v-list-item>
          <v-list-item link @click="navigateTo('/cart/client/cartClient')" prepend-icon="mdi-cart"
            title="Cart"></v-list-item>
          <v-list-item link @click="navigateTo('/orders/client/clientOrders')" prepend-icon="mdi-package"
            title="Orders"></v-list-item>
          <v-list-item link @click="navigateTo('/coupons/client/clientCoupons')" prepend-icon="mdi-package"
            title="Coupons"></v-list-item>
          <v-list-item link @click="navigateTo('/authenticator/client/profileClient')" prepend-icon="mdi-account"
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
import { ref, computed, inject, onMounted, onUnmounted } from 'vue';
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
const userType = ref(null);
const notifications = inject('notifications', ref([]));
const hasNewNotifications = inject('hasNewNotifications', ref(true));
const blogMenuOpen = ref(false);
const cartItems = ref([]);
const colorNames = {
  "#000000": "Preto",
  "#FFFFFF": "Branco",
  "#FF0000": "Vermelho",
  "#EB0909": "Vermelho",
  "#00FF00": "Verde",
  "#0000FF": "Azul",
  "#FFFF00": "Amarelo",
  "#FF00FF": "Rosa",
  "#730CF8": "Roxo",
  "#00FFFF": "Ciano",
  "#808080": "Cinza",
  // coloque aqui os HEX que seu catálogo usa
};
let pages = inject('pages', ref([]));


const snackbar = ref({
  show: false,
  text: '',
});

function parseJwt(token) {
  if (!token) throw new Error("Token JWT vazio");
  const base64Url = token.split('.')[1];
  if (!base64Url) throw new Error("Formato JWT inválido");
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );
  return JSON.parse(jsonPayload);
}


const checkAuth = () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
  isAuthenticated.value = !!token;

  if (!isAuthenticated.value) {
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_type');
    userType.value = null;
    return;
  }

  let payload = null;
  try {
    payload = parseJwt(token);
    // console.log("Payload JWT:", payload);
  } catch (err) {
    console.error("Erro ao decodificar JWT:", err);
    payload = null;
  }

  if (payload) {
    if (payload.user_id) {
      localStorage.setItem('user_id', payload.user_id);


    }
    if (payload.user_type) {
      localStorage.setItem('user_type', payload.user_type);
      userType.value = payload.user_type; // ✅ Atualiza ref reativa corretamente
      ;
    }
  } else {
    // Token inválido ou mal formatado
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_type');
    isAuthenticated.value = false;
    userType.value = null;
  }

  //  console.log("userType ref atualizado:", userType.value);
};

const isClient = computed(() => userType.value === 'client');

const getCartItems = async (payload) => {
  const token = localStorage.getItem("access_token") || localStorage.getItem("token");
  if (!token) {
    console.warn("Usuário não autenticado, não é possível buscar o carrinho.");
    return;
  }

  let userId = localStorage.getItem('user_id');
  if (!userId) {
    const payload = parseJwt(token);
    userId = payload?.user_id || payload?.sub || null;
    if (userId) {
      localStorage.setItem('user_id', userId);
    }
  }
  if (!userId) {
    console.warn("User ID não encontrado");
  }
  try {

    const response = await api.get(`/cart/get-cart/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    cartItems.value = response.data;


  }
  catch (e) {
    console.log('nenhum item encontrado...', e);
  }
}

//const updateQuantity = async (item) => {
//  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
//  if(!token){
//    return;
//  }
//
//  try{
//    const response = await 
//  }
//  catch(e){}
//}

onMounted(async () => {
  getPages();
  getCartItems();
  try {
    const res = await api.get('/config/config');
    logoUrl.value = res.data.logo_url;
  }
  catch (error) {
    console.error("Erro ao carregar logo:", error);
  }
  checkAuth();
  userType.value = localStorage.getItem('user_type'); // pega do localStorage depois
  //console.log("User type inicial:", userType.value);
  window.addEventListener('storage', checkAuth);


});


onUnmounted(() => {
  window.removeEventListener('storage', checkAuth);

});



const showNotifications = () => {
  hasNewNotifications.value = false;
  fetchNotifications();

};

const showCartItems = async () => {
  await getCartItems();
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

const removeItem = async (item) => {
  if (!confirm("Tem certeza que deseja remover este produto do carrinho ?")) return;
  try {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');

    const itemId = item.id;
    const response = await api.delete(`/cart/cart-item-remove/${itemId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (response.status === 200) {
      cartItems.value = cartItems.value.map(cart => ({ ...cart, items: cart.items.filter(i => i.id !== itemId) }));
      console.log('Item removido');

    }
  }
  catch (e) {
    console.log("Erro ao remover item", e.error);
  }

};

const checkout = (item) => {
  sessionStorage.setItem('checkout_item', JSON.stringify(item));
  router.push('/payments/client/checkout');
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