from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# ============================================
# CONFIGURACIÓN BASE DE DATOS - VERSIÓN FINAL
# ============================================

# 1. Obtener credenciales
DB_HOST = os.environ.get('DB_HOST', 'mysql-2b45c406-alex-74a3.j.aivencloud.com')
DB_USER = os.environ.get('DB_USER', 'avnadmin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'AVNS_nUGv/Me6QC6X-Ax4VNF')
DB_PORT = os.environ.get('DB_PORT', '15361')
DB_NAME = os.environ.get('DB_NAME', 'defaultdb')

print("📊 Configurando base de datos...")

# 2. Codificar la contraseña
encoded_password = quote_plus(DB_PASSWORD)

# 3. Crear URL de conexión - SIN PARÁMETROS SSL EN LA URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"✅ URL creada: mysql+pymysql://{DB_USER}:******@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 4. Configurar SSL usando connect_args (no en la URL)
connect_args = {}
if DB_HOST.endswith('aivencloud.com'):  # Si es Aiven
    connect_args = {
        'ssl': {
            'ca': '/etc/ssl/certs/ca-certificates.crt'
        }
    }
    print("🔒 SSL configurado para Aiven")

# 5. Crear motor de base de datos
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,  # SSL va aquí
        pool_pre_ping=True,
        pool_recycle=280,
        pool_size=5,
        echo=False
    )
    print("✅ Engine creado exitosamente")
except Exception as e:
    print(f"❌ Error creando engine: {e}")
    
    # Fallback para desarrollo local
    print("🔄 Probando MySQL local...")
    engine = create_engine(
        "mysql+pymysql://root:12345@localhost:3306/db_cc",
        pool_pre_ping=True
    )

# 6. Configurar sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 7. Función para obtener conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()