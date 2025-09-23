import fs from 'fs';
import axios from 'axios';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const API_URL = 'https://rua11store-catalog-api-lbp7.onrender.com';
const SITE_URL = 'https://rua11store-catalog-api.vercel.app';

async function generateSitemap() {
  try {
    const staticPages = ['', '/', '/sobre'];

    const urls = staticPages.map(route => `
  <url>
    <loc>${SITE_URL}${route}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
  </url>`);

    // Produtos
    const produtosRes = await axios.get(`${API_URL}/product-seo`);
    const produtos = produtosRes.data;

    produtos.forEach(produto => {
      if (produto.slug) {
        urls.push(`
  <url>
    <loc>${SITE_URL}/products/productView/${encodeURIComponent(produto.slug)}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
  </url>`);
      }
    });

    // Posts do blog
    const postsRes = await axios.get(`${API_URL}/blog/posts`);
    const posts = postsRes.data;

    for (const post of posts) {
      let seo = {};
      try {
        const seoRes = await axios.get(`${API_URL}/post-seo/post_seo/${post.id}`);
        if (!seoRes.data.error) {
          seo = seoRes.data; // contém apenas campos SEO
        }
      } catch (err) {
        console.warn(`⚠️ SEO não encontrado para post ID ${post.id}`);
      }

      const lastmod = post.updated_at || post.created_at || new Date().toISOString();
      const canonical = seo.canonical_url || `${SITE_URL}/blog/blogView/${encodeURIComponent(post.slug)}`;

      urls.push(`
  <url>
    <loc>${SITE_URL}/blog/blogView/${encodeURIComponent(post.slug)}</loc>
    <lastmod>${new Date(lastmod).toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`);
    }

    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>`;

    const publicDir = path.resolve(__dirname, 'public');
    if (!fs.existsSync(publicDir)) fs.mkdirSync(publicDir);

    fs.writeFileSync(path.resolve(publicDir, 'sitemap.xml'), sitemap.trim());
    console.log('✅ sitemap.xml gerado com sucesso!');
  } catch (error) {
    console.error('❌ Erro ao gerar sitemap:', error.message);
  }
}

generateSitemap();
