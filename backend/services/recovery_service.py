from datetime import datetime, timedelta
from services.cart_service import get_supabase
from controllers.emailController import EmailController
from extensions import email_controller
from services.fcm_service import send_fcm_notification
import logging
import requests
import json

logger = logging.getLogger("recovery_service")
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class RecoveryService:
    @staticmethod
    def check_and_send_recovery_emails(app, hours=24):
        with app.app_context():
            supabase = get_supabase(service=True)
            limit_time = datetime.utcnow() - timedelta(hours=hours)

            all_carts = (
                supabase.table("carts")
                .select("*")
                .eq('status', 'active')
                .is_("recovery_sent_at", None)
                .execute()
                .data
            )
            
            abandoned_carts = []
            for c in all_carts:
                updated_at = datetime.fromisoformat(c['updated_at'].split('+')[0])
                if updated_at < limit_time:
                    abandoned_carts.append(c)
            
            for cart in abandoned_carts:
                user = (
                    supabase.table("user_profiles")
                    .select("email, full_name")
                    .eq("user_id", cart["user_id"])
                    .maybe_single()
                    .execute()
                    .data
                )
                
                
                if not user or not user.get("email"):
                    print(f"[DEBUG] Carrinho {cart['id']} ignorado: usuário sem email")
                    continue

                cart_items = (
                    supabase.table('cart_items')
                    .select('*')
                    .eq('cart_id', cart['id'])
                    .execute()
                    .data
                )

                if not cart_items:
                    continue

                items_list_html = ""
                for item in cart_items:
                    item_name = item.get('product_name', 'Produto')
                    item_price = item.get('price', 0)
                    quantity = item.get("quantity", 1)
                    items_list_html += f"<li>{item_name} - R$ {item_price:.2f} (Qtd: {quantity})</li>"
                subject = "🛒 Você esqueceu seu carrinho na Rua11Store!"
                recipients = [user["email"]]
                body = f"Olá {user.get('full_name', '')}, você deixou alguns itens no carrinho."
                html = f"""
                    <p>Olá {user.get('full_name', '')} 👋</p>
                    <p>Você deixou o seguinte item no seu carrinho:</p>
                    <ul><li>{items_list_html}</li></ul>
                    <p><a href="https://rua11store-web.vercel.app/"
                        style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;">
                        Finalizar Compra</a></p>
                """

                #lock cart
                updated = (
                    supabase.table('carts').update({
                        "status": "pending_recovery",
                        "recovery_sent_at": datetime.utcnow().isoformat(),
                        "lock": True
                    })
                    .eq("id", cart["id"])
                    .eq("lock", False)
                    .execute()
                    .data
                )
               

                if not updated:
                    # other work get this cart
                    continue
                
                try:
                    EmailController.send_email(subject, recipients, body, html)

                    tokens = (
                        supabase.table('user_devices')
                            .select('device_token')
                            .eq('user_id', cart['user_id'])
                            .execute()
                            .data
                    )
                   

                    if user.get('device_token'):
                        supabase.table("carts").update({
                            "status": "abandoned",
                            "recovery_sent_at": datetime.utcnow().isoformat()
                        }).eq("id", cart['id']).execute()
                    
                    if tokens:
                        for token in tokens:
                            device_token = token.get("device_token")
                            if not device_token:
                                continue
                            
                            send_fcm_notification(
                                token=device_token,
                                title="🛒 Você esqueceu seu carrinho!" ,
                                body="Finalize sua compra antes que acabe o estoque 🚀",
                                data={"cart_id": cart["id"]},
                                link="google.com"
                            )


                    logger.info(f"E-mail enviado para {user['email']} - carrinho {cart['id']}")
                except Exception:
                    # revert lock if fail
                    supabase.table('carts').update({
                        "status": "active",
                        "recovery_sent_at": None
                    }).eq("id", cart['id']).execute()

                    logger.error(f"Falha ao enviar email para {user['email']}", exc_info=True)
