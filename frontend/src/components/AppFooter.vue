<template>
  <v-footer color="purple-darken-4" class="text-center d-flex flex-column ga-2 py-4">
    <div class="d-flex ga-3">
      <a v-for="item in social_links" :key="item.title" :href="item.href" :title="item.title"
          class="d-inline-block social-link " rel="noopener noreferrer" target="_blank" >
      <v-icon :icon="item.icon" :size="item.icon === '$vuetify' ? 24 : 16" />
    </a>
    </div>
    
    <v-divider class="my-0" thickness="2" width="50"></v-divider>
    
    <div class="text-caption font-weight-regular opacity-60" color="surface-light">
      
      <v-btn v-for="link in items" :key="link.title" :text="link.name" variant="text" rounded 
        class="" @click="navigateToPage(link)"></v-btn>

    </div>
    <v-divider></v-divider>

    <div>
        <span class="d-none d-sm-inline-block">Rua11Store</span>  &copy; 2022-{{ (new Date()).getFullYear() }} 
    </div>

  </v-footer>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';

const router = useRouter();

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
    : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});

onMounted(async () => {
  try {
    const response = await api.get('/pages/pages')
    items.value = response.data.pages.sort((a: PageItem, b: PageItem) => {
      if(a.name === 'Home Page') return -1;
      if(b.name === 'Home Page') return 1;
      return 0;
    })

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
  // {
  //   title: 'Rua11Store Whatsapp',
  //   icon: 'mdi-whatsapp',
  //   href: 'https://rua11store.com',
  // }
]

const navigateToPage = (link: PageItem) => {
  if (link.name === 'Home Page') {
    router.push('/')
  } else {
    router.push(`/menagementPage/pageView/${link.id}`);
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
