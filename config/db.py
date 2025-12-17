from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# ==================================================
# CONFIGURACIÓN DE BASE DE DATOS (PRODUCCIÓN SEGURA)
# ==================================================

print("📊 Configurando conexión a la base de datos...")

# 1. Leer variables de entorno (OBLIGATORIO)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# 2. Validar que existan todas
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    raise RuntimeError("❌ Variables de entorno de base de datos no configuradas")

# 3. Codificar contraseña (por caracteres especiales)
encoded_password = quote_plus(DB_PASSWORD)

# 4. Crear URL de conexión
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print(f"✅ Conectando a DB en host: {DB_HOST}")

# 5. Configurar SSL (Aiven requiere SSL)
connect_args = {}

if DB_HOST.endswith("aivencloud.com"):
    connect_args = {
        "ssl": {
            "ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    }
    print("🔒 SSL habilitado para Aiven")

# 6. Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=280,
    pool_size=5,
    max_overflow=10,
    echo=False
)

print("✅ Engine de SQLAlchemy creado correctamente")

# 7. Configurar sesión y base
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# 8. Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
