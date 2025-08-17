import os
from flask import Blueprint, jsonify, url_for, send_from_directory, current_app

upload_images_bp = Blueprint('uploadImages', __name__)

@upload_images_bp.route('/uploads', methods=['GET'])
def list_uploads():
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    files = []
    for filename in os.listdir(upload_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            files.append({
                "name": filename,
                "url": url_for('uploadImages.uploaded_file', filename=filename, _external=True)
            })
    return jsonify(files)

@upload_images_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_folder, filename)
