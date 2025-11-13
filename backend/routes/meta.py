import requests
from flask import Flask, Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv

meta_bp = Blueprint('meta', __name__)

@meta_bp.route("/meta/conversion", methods=["POST"])
def meta_conversion():
    data = request.json
    event_name = data.get("event_name", "Purchase")
    event_id = data.get("event_id")  # mesmo ID usado no front-end

    payload = {
        "data": [{
            "event_name": event_name,
            "event_time": int(__import__("time").time()),
            "event_id": event_id,
            "action_source": "website",
            "event_source_url": data.get("event_source_url"),
            "user_data": {
                "em": data.get("email_hash"),  # SHA256 do e-mail
                "ph": data.get("phone_hash"),  # SHA256 do telefone
                "client_ip_address": request.remote_addr,
                "client_user_agent": request.headers.get("User-Agent"),
            },
            "custom_data": {
                "currency": "BRL",
                "value": data.get("value"),
                "contents": data.get("contents", []),
                "content_type": "product"
            }
        }],
        "access_token": os.getenv("META_ACCESS_TOKEN")
    }

    response = requests.post(os.getenv("CONVERSIONS_API_URL"), json=payload)
    return jsonify(response.json())

