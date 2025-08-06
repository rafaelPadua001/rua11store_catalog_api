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
    : 'https://rua11store-catalog-api-lbp7.onrender.com'

    metaTitle.value = data.metaTitle ||  data.seo.meta_title || ''
    metaDescription.value = data.metaDescription || data.seo.meta_description || ''
    metaKeywords.value = data.metaKeywords || data.seo.meta_keywords || ''
    ogTitle.value = data.ogTitle || data.seo.meta_title || ''
    ogDescription.value = data.ogDescription || data.seo.meta_description || ''
    ogImage.value =  ogImage.value = data.ogImage ? `${data.ogImage}` : data.thumbnail_path || '' 
  }

  return { setSeo }
}
