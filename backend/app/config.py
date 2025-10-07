import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "uma-chave-secreta-muito-segura"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "postgresql://regiflex_user:password123@db:5432/regiflex_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:3000",  # Frontend development
        "http://localhost:5173",  # Vite development server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://frontend:5173",   # Docker frontend service
        "http://frontend:3000",   # Docker frontend service (alternative)
        "http://regiflex_frontend:5173",  # Docker container name
        "http://regiflex_frontend:3000"   # Docker container name (alternative)
    ]

