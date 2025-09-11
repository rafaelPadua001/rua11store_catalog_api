# services/fcm_service.py
import requests
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLIC_ANON_KEY")
FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
FCM_URL = "https://fcm.googleapis.com/v1/projects/rua11store-notifications-24f29/messages:send"

def send_fcm_notification(token: str, title: str, body: str, link: str):
    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": token,
        "notification": {
            "title": title,
            "body": body
        },
        "webpush": {
            "fcm_options": {
                "link": link
            }
        }
    }
    resp = requests.post(FCM_URL, headers=headers, json=payload)
    return resp

def send_notification_to_all_users(title: str, body: str, link: str):
    response = supabase.table("user_devices").select("device_token").execute()
    tokens = [row["device_token"] for row in response.data if row.get("device_token")]
    
    for token in tokens:
        resp = send_fcm_notification(token, title, body, link)
        print(f"Enviando para {token[:8]}..., status: {resp.status_code}")
