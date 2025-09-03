from datetime import datetime, timedelta
from services.cart_service import get_supabase

class AbandonedCart:
    @staticmethod
    def get_abandoned_cart(hours: int = 24):
        supabase = get_supabase(service=True)
        response = supabase.table("public.cart").select("*").execute()
      
