import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Supabase
    SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_PUBLIC_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_PROJECT_SERVICE_ROLE_KEY")

     #Gmail SMTP
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "t")
    MAIL_USERNAME = os.getenv("GMAIL_USERNAME", "comercialrua11store@gmail.com")
    MAIL_PASSWORD = os.getenv("GMAIL_PASSWORD", "tlbubwlfunsrfsyd")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "comercialrua11store@gmail.com")