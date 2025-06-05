import { ref } from 'vue'
import { useHead } from '@vueuse/head'

export function useSeo() {
  const metaTitle = ref('')
  const metaDescription = ref('')
  const metaKeywords = ref('')
  const ogTitle = ref('')
  const ogDescription = ref('')
  const ogImage = ref('')

  useHead({
    title: metaTitle,
    meta: [
      { name: 'description', content: metaDescription },
      { name: 'keywords', content: metaKeywords },
      { property: 'og:title', content: ogTitle },
      { property: 'og:description', content: ogDescription },
      { property: 'og:image', content: ogImage },
    ],
  })

  function setSeo(data: any) {
      const baseURL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://rua11store-catalog-api.onrender.com'

    metaTitle.value = data.metaTitle || ''
    metaDescription.value = data.metaDescription || ''
    metaKeywords.value = data.metaKeywords || ''
    ogTitle.value = data.ogTitle || ''
    ogDescription.value = data.ogDescription || ''
    ogImage.value =  ogImage.value = data.ogImage ? `${baseURL}/${data.ogImage}` : ''
  }

  return { setSeo }
}
