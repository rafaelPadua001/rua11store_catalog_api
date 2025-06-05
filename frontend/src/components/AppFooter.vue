<template>
  <v-footer height="40" app color="purple-darken-4" class="d-flex align-center justify-between px-4">
    <a v-for="item in social_links" :key="item.title" :href="item.href" :title="item.title"
      class="d-inline-block mx-2 social-link " rel="noopener noreferrer" target="_blank">
      <v-icon :icon="item.icon" :size="item.icon === '$vuetify' ? 24 : 16" />
    </a>

    <div class="d-flex align-center justify-start ga-2 flex-wrap flex-grow-1 py-3 text-disabled " color="surface-light">
      <v-btn v-for="link in items" :key="link.title" :text="link.name" variant="text" rounded size="x-small"
        class="social-link-btn" @click="navigateToPage(link)"></v-btn>

    </div>

    <div class="text-caption text-disabled" style="position: absolute; right: 16px;">
  &copy; 2022-{{ (new Date()).getFullYear() }} <span class="d-none d-sm-inline-block">Rua11Store</span>
</div>

  </v-footer>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface PageItem {
  id: string;
  title: string;
  name: string;
  // href: string;
}

const items = ref<PageItem[]>([])

const api = axios.create({
  baseURL: window.location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://rua11store-catalog-api.onrender.com",
  headers: { "Content-Type": "application/json" },
});

onMounted(async () => {
  try {
    const response = await api.get('/pages/pages')
    items.value = response.data.pages

  } catch (error) {
    console.error('Error fetching social links:', error)
  }
});

const social_links = [

  {
    title: 'Rua11Store Support',
    icon: 'mdi-help-circle-outline',
    href: 'https://rua11store.com',
  },
  {
    title: 'Rua11Store Mail',
    icon: 'mdi-mail',
    href: 'https://rua11store.com',
  },
  {
    title: 'Rua11Store Instagram',
    icon: 'mdi-instagram',
    href: 'https://www.instagram.com/rua11store.tab?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==',
  },
  {
    title: 'Rua11Store Facebook',
    icon: 'mdi-facebook',
    href: 'https://rua11store.com',
  },
  {
    title: 'Rua11Store Whatsapp',
    icon: 'mdi-whatsapp',
    href: 'https://rua11store.com',
  }
]

const navigateToPage = (link: PageItem) => {
  if (link.name === 'Home Page') {
    window.location.href = '/';
  } else {
    window.location.href = `/menagementPage/pageView/${link.id}`;
  }
}
</script>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: white
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgba(25, 118, 210, 1)

  .social-link-btn
    color: white
    text-decoration: none
    transition: .2s ease-in-out
    cursor: pointer

    &:hover
      color: rgba(25, 118, 210, 1)
  
  .text-caption.text-disabled
    color: white !important
</style>
