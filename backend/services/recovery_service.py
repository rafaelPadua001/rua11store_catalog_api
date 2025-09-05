from datetime import datetime, timedelta
from services.cart_service import get_supabase
from controllers.emailController import EmailController
from extensions import email_controller
import logging


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
                supabase.table("cart")
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
                    continue

                subject = "🛒 Você esqueceu seu carrinho na Rua11Store!"
                recipients = [user["email"]]
                body = f"Olá {user.get('full_name', '')}, você deixou alguns itens no carrinho."
                html = f"""
                    <p>Olá {user.get('full_name', '')} 👋</p>
                    <p>Você deixou o seguinte item no seu carrinho:</p>
                    <ul><li>{cart['product_name']} - R$ {cart['price']/100:.2f}</li></ul>
                    <p><a href="https://rua11store.com/carrinho/{cart['id']}"
                        style="background:#000;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;">
                        Finalizar Compra</a></p>
                """

                #lock cart
                updated = (
                    supabase.table('cart').update({
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

                    supabase.table("cart").update({
                        "status": "abandoned",
                        "recovery_sent_at": datetime.utcnow().isoformat()
                    }).eq("id", cart['id']).execute()

                    logger.info(f"E-mail enviado para {user['email']} - carrinho {cart['id']}")
                except Exception:
                    # revert lock if fail
                    supabase.table('cart').update({
                        "status": "active",
                        "recovery_sent_at": None
                    }).eq("id", cart['id']).execute()

                    logger.error(f"Falha ao enviar email para {user['email']}", exc_info=True)
