from datetime import datetime, timedelta
from flask import current_app
from services.cart_service import get_supabase
from controllers.emailController import EmailController
from extensions import email_controller

class RecoveryService:
    @staticmethod
    def check_and_send_recovery_emails(hours=24):
        supabase = get_supabase(service=True)
        limit_time = datetime.utcnow() - timedelta(hours=hours)

        # Busca todos os carrinhos ativos
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
            updated_at = datetime.fromisoformat(c['updated_at'].split('+')[0])  # remove timezone se existir
            if updated_at < limit_time:
                abandoned_carts.append(c)

        

        for cart in abandoned_carts:
            user = supabase.table("user_profiles").select("email, full_name").eq("user_id", cart["user_id"]).maybe_single().execute().data
            if not user or not user.get("email"):
                continue

            subject = "🛒 Você esqueceu seu carrinho na Rua11Store!"
            recipients = [user["email"]]
            body = f"Olá {user.get('full_name', '')}, você deixou alguns itens no carrinho."
            html = f"""
                <p>Olá {user.get('full_name', '')} 👋</p>
                <p>Você deixou o seguinte item no seu carrinho:</p>
                <ul>
                    <li>{cart['product_name']} - R$ {cart['price']/100:.2f}</li>
                </ul>
                <p>
                    <a href="https://rua11store.com/carrinho/{cart['id']}"
                       style="background:#000;color:#fff;padding:10px 20px;
                              text-decoration:none;border-radius:5px;">
                       Finalizar Compra
                    </a>
                </p>
            """

            try:
                EmailController.send_email(subject, recipients, body, html)

                #match cart with processed
                supabase.table("cart").update({
                    "status": "abandoned",
                    "recovery_sent_at": datetime.utcnow().isoformat()
                }).eq("id", cart['id']).execute()

                
                current_app.logger.info(f"E-mail enviado para {user['email']} - carrinho {cart['id']}")
            except Exception as e:
                current_app.logger.error(f"Falha ao enviar email para {user['email']}: {e}")
            
