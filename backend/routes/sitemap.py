from email.mime import base
from flask import Blueprint, Response
from datetime import datetime
from database import db
from models.product import Product
from models.productSeo import ProductSeo

sitemap_bp = Blueprint('sitemap', __name__)
@sitemap_bp.route('/sitemap.xml')
def sitemap():
    base_url = "https://rua11store-catalog-api-lbp7.onrender.com"

    urls = []

    # URLs estáticas
    urls.append({
        'loc': f"{base_url}/",
        'lastmod': datetime.utcnow().date().isoformat()
    })
    urls.append({
        'loc': f"{base_url}/sobre",
        'lastmod': datetime.utcnow().date().isoformat()
    })

    # URLs dinâmicas de produtos
    produtos = db.session.query(Product).join(ProductSeo).all()

    for produto in produtos:
        if produto.seo and produto.seo.slug:
            urls.append({
                'loc': f"{base_url}/produto/{produto.seo.slug}",
                'lastmod': produto.updated_at.date().isoformat() if hasattr(produto, 'updated_at') and produto.updated_at else datetime.utcnow().date().isoformat()

            })

    # Monta o XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        xml.append('  <url>')
        xml.append(f"    <loc>{url['loc']}</loc>")
        xml.append(f"    <lastmod>{url['lastmod']}</lastmod>")
        xml.append('  </url>')

    xml.append('</urlset>')

    return Response("\n".join(xml), mimetype='application/xml')

@sitemap_bp.route('/robots.txt')
def robots_txt():
    base_url = "https://rua11store-catalog-api-lbp7.onrender.com"

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base_url}/sitemap.xml"
    )
    return Response(content, mimetype='text/plain')