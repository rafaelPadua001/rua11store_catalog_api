from flask import Blueprint, request, jsonify, session, current_app, send_from_directory
from controllers.couponController import CouponController
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

coupon_bp = Blueprint('coupon', __name__)

@coupon_bp.route('/coupons', methods=['GET'])
@jwt_required()
def get_coupons():
    #user_id = get_jwt_identity()
    coupon_controller = CouponController()
    try:
        coupons = coupon_controller.get_all_coupons()
        coupons_dict = [coupon.to_dict() for coupon in coupons]
        return jsonify(coupons_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@coupon_bp.route('/promotional_coupons', methods=['GET'])
def get_promotional_coupons():
    coupon_controller = CouponController()
    try:
        coupons = coupon_controller.get_promotional_coupons()
        coupons_dict = [coupon.to_dict() for coupon in coupons]
        return jsonify(coupons_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@coupon_bp.route('/get-all-client-coupons', methods=['GET'])
def get_coupons_all():
    #user_id = get_jwt_identity()
    coupon_controller = CouponController()
    try:
        coupons = coupon_controller.get_all_coupons()
        coupons_dict = [coupon.to_dict() for coupon in coupons]
        return jsonify(coupons_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@coupon_bp.route('/create_coupon', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_coupon():
    if request.method == 'OPTIONS':
        return '', 200

    user_id = get_jwt_identity()

    client_id = request.form.get('client_id')
    client_username = request.form.get('client_username')
    client_email = request.form.get('client_email')
    title = request.form.get('title')
    code = request.form.get('code')
    discount = request.form.get('discount')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    image = request.files.get('image')

    image_path = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        image_folder = os.path.join(current_app.root_path, 'uploads/coupons')
        os.makedirs(image_folder, exist_ok=True)
        full_path = os.path.join(image_folder, filename)
        image.save(full_path)
        image_path = f'/uploads/coupons/{filename}'

    coupon_controller = CouponController()
    try:
        coupon = coupon_controller.create_coupon(
            user_id=user_id,
            client_id=client_id,
            client_username=client_username,
            client_email=client_email,
            title=title,
            code=code,
            discount=discount,
            start_date=start_date,
            end_date=end_date,
            image_path=image_path
        )
        return jsonify({
            'message': 'Cupom criado com sucesso!',
            'coupon': coupon
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@coupon_bp.route('/<int:coupon_id>', methods=['PUT'])
@jwt_required()
def update_coupon(coupon_id):
    # from flask import request  # <--- Garante que a variável request está definida
    user_id = get_jwt_identity()
    coupon_controller = CouponController()

    try:
        # Pode ser request.form (form-data) ou request.get_json() (JSON)
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        client_id_raw = data.get('client_id')
        client_id = client_id_raw if client_id_raw not in [None, '', 'null'] else None

        title = data.get('title')
        code = data.get('code')
        discount = data.get('discount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Converte types se necessário
        discount = float(discount) if discount else 0.0

        image_file = request.files.get('image')
        image_path = None

        if image_file:
            filename = secure_filename(image_file.filename)
            upload_dir = os.path.join(os.getcwd(), 'uploads/coupons')
            os.makedirs(upload_dir, exist_ok=True)
            full_image_path = os.path.join(upload_dir, filename)
            image_file.save(full_image_path)

            # Mas grava no banco só o caminho relativo
            image_path = f'/uploads/coupons/{filename}'

        coupon = coupon_controller.update_coupon(
            coupon_id,
            user_id,
            client_id,
            title,
            code,
            discount,
            start_date,
            end_date,
            image_path
        )

        if not coupon:
            return jsonify({'error': 'Cupom não encontrado.'}), 404

        return jsonify(coupon), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@coupon_bp.route('/uploads/<path:filename>')
def serve_uploads(filename):
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    return send_from_directory(uploads_dir, filename)

@coupon_bp.route('/uploads/coupons/<path:filename>')
def serve_coupon_uploads(filename):
    uploads_dir = os.path.join(current_app.root_path, 'uploads', 'coupons')
    return send_from_directory(uploads_dir, filename)

@coupon_bp.route('/pick_up_coupon', methods=['POST'])
def pick_up_coupon():
    data = request.get_json()
    controller = CouponController()
    response, status_code = controller.pick_up_coupon_by_client_id(data)
    return jsonify(response), status_code

@coupon_bp.route('/get-coupons/<string:user_id>', methods=['GET'])
def get_coupons_by_user(user_id):
    coupon_controller = CouponController()
    try:
        coupons = coupon_controller.get_coupons_by_user(user_id)
      
        return jsonify(coupons), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@coupon_bp.route('/delete-coupons-by-client/<string:coupon_id>', methods=['DELETE'])
def delete_coupons_by_client(coupon_id):
    user_id = request.args.get('userId')

    if not user_id:
        return jsonify({'error': 'user_id é obrigatório.'}), 400
    
    coupon_controller = CouponController()
    try:
        success = coupon_controller.delete_coupons_by_client(coupon_id, user_id)

        if success:
            return jsonify({'message': 'Cupons deletados com sucesso!'}), 200
        else:
            return jsonify({'error': 'Nenhum cupom encontrado para este cliente.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
@coupon_bp.route('/<int:coupon_id>', methods=['DELETE'])
@jwt_required()
def delete_coupon(coupon_id):
    coupon_controller = CouponController()
    try:
        success = coupon_controller.delete_coupon(coupon_id)
        if success:
            return jsonify({'message': 'Cupom deletado com sucesso!'}), 200
        else:
            return jsonify({'error': 'Cupom não encontrado.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400