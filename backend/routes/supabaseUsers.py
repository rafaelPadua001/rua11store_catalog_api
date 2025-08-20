from flask import Blueprint, request, jsonify
from supabase import create_client
import os

supabaseUsers_bp = Blueprint("supabaseUsers", __name__)

url = os.getenv("SUPABASE_PROJECT_URL")
service_role_key = os.getenv("SUPABASE_PROJECT_SERVICE_ROLE_KEY")
supabase = create_client(url, service_role_key)

@supabaseUsers_bp.route("/search_users", methods=["GET"])
def search_users():
    query = request.args.get("q", "").lower()
    try:
        users_list = supabase.auth.admin.list_users()
        
        # dependendo da versão, result pode ter 'data' ou ser lista direta
        #users_list = result.get("data", result)  # pega result['data'] se existir, senão usa result

        users = [
            {
                "id": u.id,
                "email": u.email,
                "display_name": u.user_metadata.get("display_name", "")
            }
            for u in users_list
            if query in u.user_metadata.get("display_name", "").lower()
        ]

        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500