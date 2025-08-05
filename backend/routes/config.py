# routes/config.py
from flask import Blueprint, jsonify
import os

config_bp = Blueprint("config", __name__)

@config_bp.route("/config")
def get_config():
    return jsonify({
        "logo_url": os.getenv("LOGO_URL", "/uploads/logo.png")
    })
