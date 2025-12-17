from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import Base, engine
from sqlalchemy import text
from routes.usersRoutes import user
from routes.productsRoutes import product_router
from routes.interactionRoutes import interaction
from routes.training import training_router
from routes.commentsRoutes import comment_router
from routes.notification_routes import notification_routes
from routes.cartRoutes import cart_router
from routes.transaccionRoutes import transaction_router
from routes.mlsRoutes import ml_super

from seed.seed import Seeder
from seed.reset_db import DatabaseResetter
import os

# Crear las tablas si no existen (DESCOMENTA ESTO DESPUÉS)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Consumo Consciente API",
    description="API para monitorear y recomendar productos sustentables",
    version="1.0"
)

# ============================================
# 1. VERIFICAR CONEXIÓN AL INICIAR
# ============================================
@app.on_event("startup")
def startup():
    print("=" * 50)
    print("🚀 Iniciando Consumo Consciente API...")
    print(f"🌍 Entorno: {'PRODUCCIÓN' if os.environ.get('RENDER') else 'DESARROLLO'}")
    
    try:
        # Intentar conectar a la BD
        with engine.connect() as conn:
            print("✅ Conectado a Aiven MySQL")
            
            # Probar versión de MySQL
            result = conn.execute(text("SELECT VERSION() as version"))
            version = result.fetchone()[0]
            print(f"📊 MySQL Version: {version}")
    except Exception as e:
        print(f"❌ ERROR conectando a BD: {e}")
        print("⚠️  La aplicación continuará pero sin base de datos")
    
    print("=" * 50)
    
    # IMPORTANTE: Comenta esto inicialmente en producción
    # Solo descomenta cuando estés seguro que la conexión funciona
    
    # Crear tablas (descomenta después de probar conexión)
    # print("📁 Creando tablas si no existen...")
    # Base.metadata.create_all(bind=engine)
    # print("✅ Tablas creadas/verificadas")
    
    # Configuración del seeder (COMENTADO PARA PRODUCCIÓN)
    # run_reset = False   # NUNCA True en producción
    # run_seeder = False  # NUNCA True en producción
    
    # if run_reset:
    #     print("Reiniciando base de datos...")
    #     resetter = DatabaseResetter()
    #     resetter.reset()
    # 
    # if run_seeder:
    #     print("Ejecutando seeder...")
    #     seeder = Seeder()
    #     seeder.run()

# ============================================
# 2. HABILITAR CORS
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 🔥 IMPORTANTE
    allow_credentials=False,      # 🔥 OBLIGATORIO
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 3. REGISTRAR TODAS TUS RUTAS
# ============================================
app.include_router(product_router)
app.include_router(user)
app.include_router(interaction)
app.include_router(training_router)
app.include_router(comment_router)
app.include_router(notification_routes)
app.include_router(cart_router)
app.include_router(transaction_router)
app.include_router(ml_super)

# ============================================
# 4. ENDPOINTS DE PRUEBA Y SALUD
# ============================================
@app.get("/")
async def root():
    return {
        "message": "Consumo Consciente API",
        "status": "online",
        "version": "1.0",
        "docs": "/docs",
        "health_check": "/health",
        "test_db": "/test-db"
    }

@app.get("/health")
async def health():
    """Endpoint de salud para monitoreo"""
    from config.db import engine
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "ok",
        "database": db_status,
        "timestamp": "2024-01-01T00:00:00Z"  # Usar datetime en producción
    }

@app.get("/test-db")
def test_db():
    """Endpoint para probar conexión a base de datos"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 'Conexión exitosa' as message, VERSION() as version"))
            row = result.fetchone()
            return {
                "status": "success", 
                "message": row[0],
                "mysql_version": row[1]
            }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "suggestion": "Verifica las variables DB_HOST, DB_USER, DB_PASSWORD en Render"
        }
