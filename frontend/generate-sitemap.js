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
    const staticPages = [
      '',
      '/',
      '/sobre'

    ];

    const urls = staticPages.map(route => `
  <url>
    <loc>${SITE_URL}${route}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
  </url>`);

    const response = await axios.get(`${API_URL}/product-seo`);
    const produtos = response.data;

    produtos.forEach(produto => {
      if (produto.slug) {
        urls.push(`
  <url>
    <loc>${SITE_URL}/products/productView/${encodeURI(produto.slug)}</loc>

    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
  </url>`);
      }
    });

    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>`;

    fs.writeFileSync(path.resolve(__dirname, 'public', 'sitemap.xml'), sitemap.trim());
    console.log('✅ sitemap.xml gerado com sucesso!');
  } catch (error) {
    console.error('❌ Erro ao gerar sitemap:', error.message);
  }
}

generateSitemap();
