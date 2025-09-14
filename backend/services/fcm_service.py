# services/fcm_service.py
import os
import requests
from supabase import create_client, Client
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from tempfile import NamedTemporaryFile
import json



# Carrega variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLIC_ANON_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # caminho JSON da conta de serviço

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

service_account_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if service_account_json:
    try:
        # valida que é JSON válido
        creds_dict = json.loads(service_account_json)
        with NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(json.dumps(creds_dict).encode())
            f.flush()
            SERVICE_ACCOUNT_FILE = f.name
    except json.JSONDecodeError:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS no .env não está em formato JSON válido")

# URL base do FCM v1
FCM_URL = f"https://fcm.googleapis.com/v1/projects/rua11store-notifications-24f29/messages:send"


def get_access_token():
    """Gera o access_token do service account para autenticar no FCM v1"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    auth_req = Request()
    creds.refresh(auth_req)
    return creds.token


def send_fcm_notification(token: str, title: str, body: str, link: str, data: dict = None):
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            },
            "webpush": {
                "fcm_options": {"link": link},
                "notification": {"click_action": link}
            },
            "data": data or {}
        }
    }
    resp = requests.post(FCM_URL, headers=headers, json=payload)
    return resp


def send_notification_to_all_users(title: str, body: str, link: str, data: dict = None):
    response = supabase.table("user_devices").select("device_token").execute()
    tokens = [row["device_token"] for row in response.data if row.get("device_token")]

    for token in tokens:
        resp = send_fcm_notification(token, title, body, link,)
        print(f"Enviando para {token[:8]}..., status: {resp.status_code}, resp: {resp.text}")
