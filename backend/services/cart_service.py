from supabase import create_client
from config import Config

def get_supabase(service=False):
    """
    Retorna o cliente Supabase.
    Se service=True, usa a Service Role Key para ignorar RLS.
    """
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_SERVICE_ROLE_KEY if service else Config.SUPABASE_ANON_KEY
    
    return create_client(url, key)
