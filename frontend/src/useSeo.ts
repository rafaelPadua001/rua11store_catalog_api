import { ref } from 'vue'
import { useHead } from '@vueuse/head'

export function useSeo() {
  const metaTitle = ref('')
  const metaDescription = ref('')
  const metaKeywords = ref('')
  const ogTitle = ref('')
  const ogDescription = ref('')
  const ogImage = ref('')
  const canonicalUrl = ref('')

  useHead({
    title: metaTitle,
    meta: [
      {name: 'title', content: metaTitle},
      { name: 'description', content: metaDescription },
      { name: 'keywords', content: metaKeywords },
      { property: 'og:title', content: ogTitle },
      { property: 'og:description', content: ogDescription },
      { property: 'og:image', content: ogImage },
    ],
    link: [
      {
        rel: 'canonical', href: canonicalUrl
      },
    ],
  })

  function setSeo(data: any) {
      const baseURL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://rua11store-catalog-api-lbp7.onrender.com'

    metaTitle.value = data.metaTitle ||  data.seo?.meta_title || data.post?.title || ''
    metaDescription.value = data.metaDescription || data.seo?.meta_description || data.post?.excerpt || ''
    metaKeywords.value = data.metaKeywords || data.seo?.meta_keywords ||  data.seo?.keywords  || ''
    ogTitle.value = data.ogTitle || data.seo?.og_title || data.post?.title || ''
    ogDescription.value = data.ogDescription || data.seo?.meta_description || data.post?.excerpt || ''
    ogImage.value =  ogImage.value = data.ogImage ? `${data.ogImage}` : data.thumbnail_path || data.post?.cover_image || '' 
    canonicalUrl.value = data.canonicalUrl || data.seo?.canonical_url || `${window.location.origin}/blog/${data.post?.id}`
  }

  return { setSeo }
}
