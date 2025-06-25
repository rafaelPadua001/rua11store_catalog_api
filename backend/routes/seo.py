from flask import Blueprint, jsonify, request
from controllers.seoController import SeoController
from werkzeug.utils import secure_filename
import os
import cloudinary
import cloudinary.uploader

seo_bp = Blueprint('seo', __name__)
@seo_bp.route('/seo', methods=['GET'])
def list_seo():
    seo = SeoController.get_all_seo()
    return jsonify({"seo": seo}), 200

@seo_bp.route('/seo/<int:seo_id>', methods=['GET'])
def get_seo_by_id(seo_id):
    seo = SeoController.get_seo_by_route(seo_id)
    if  seo is None:
        return jsonify({"error": "SEO item not found"}), 404
    return jsonify({"seo": seo.to_dict()}), 200

@seo_bp.route('/seo', methods=['POST'])
def create_seo():
    # Receber dados do formulário (exceto imagem)
    route = request.form.get('route')
    meta_title = request.form.get('metaTitle')
    meta_description = request.form.get('metaDescription')
    meta_keywords = request.form.get('metaKeywords')
    og_title = request.form.get('ogTitle')
    og_description = request.form.get('ogDescription')

    # Receber imagem (arquivo ou URL)
    og_image_file = request.files.get('ogImage')
    og_image_url = request.form.get('ogImageUrl')  

    if not all([route, meta_title, meta_description, meta_keywords, og_title, og_description]):
        return jsonify({"error": "Missing required fields"}), 400

    og_image_path = ''

    if og_image_file:
        filename = secure_filename(og_image_file.filename)
        try:
            upload_result = cloudinary.uploader.upload(
                og_image_file,
                folder=f'seo',  # pasta no Cloudinary
                public_id=filename.rsplit('.', 1)[0],
                overwrite=True,
                resource_type='image'
            )
            og_image_path = upload_result.get("secure_url", "")
        except Exception as e:
            print(f"Erro ao fazer upload para o Cloudinary: {str(e)}")
            return jsonify({"error": "Erro ao enviar imagem"}), 500
    elif og_image_url:
        og_image_path = og_image_url
    print(og_image_path)
    seo_data = {
        "route": route,
        "metaTitle": meta_title,
        "metaDescription": meta_description,
        "metaKeywords": meta_keywords,
        "ogTitle": og_title,
        "ogDescription": og_description,
        "ogImage": og_image_path
    }
    print(seo_data)
    SeoController.save_seo(seo_data)

    return jsonify({"message": "SEO item created", "seo": seo_data}), 201

@seo_bp.route("/seoUpdate/<int:seo_id>", methods=["POST"]) 
def update_seo(seo_id):
  
    route = request.form.get("route")
    meta_title = request.form.get("metaTitle")
    meta_description = request.form.get("metaDescription")
    meta_keywords = request.form.get("metaKeywords")
    og_title = request.form.get("ogTitle")
    og_description = request.form.get("ogDescription")

    # A imagem pode vir como arquivo ou como URL
    og_image = None
    if "ogImage" in request.files:
        image_file = request.files["ogImage"]

        #update to cloudinary storage
        upload_result = cloudinary.uploader.upload(
            image_file,
            folder="seo",
           
        )
        
        og_image = upload_result.get("secure_url")
      #  og_image = f"uploads/seo/{image_file.filename}"
      #  image_file.save(og_image) 
    else:
        og_image = request.form.get("ogImageUrl")  # se for uma string


    updated_data = {
        "route": route,
        "metaTitle": meta_title,
        "metaDescription": meta_description,
        "metaKeywords": meta_keywords,
        "ogTitle": og_title,
        "ogDescription": og_description,
        "ogImage": og_image
    }
    SeoController.update_seo(seo_id, updated_data)

    return jsonify({"message": "SEO item updated", "seo": updated_data}), 200


@seo_bp.route("/seo/<int:seo_id>", methods=["DELETE"])
def delete_seo(seo_id):
    SeoController.delete_seo(seo_id)
    return jsonify({'message': 'SEO item deleted'}), 200