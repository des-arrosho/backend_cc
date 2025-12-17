from sqlalchemy import text
from config.db import SessionLocal

class DatabaseResetter:
    def __init__(self):
        self.db = SessionLocal()

    def reset(self):
        try:
            print("🧹 Limpiando base de datos y reiniciando IDs...")

            # Desactivar restricciones de claves foráneas
            self.db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

            tables = [
                "tbd_comments",
                "tbd_interactions",
                "tbb_products",
                "tbb_users",
                "tbd_cart"  # Nueva tabla agregada
            ]

            for table in tables:
                self.db.execute(text(f"TRUNCATE TABLE {table}"))
                print(f"✓ Tabla {table} truncada")

            # Reactivar restricciones
            self.db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

            # Reiniciar AUTO_INCREMENT (aunque TRUNCATE ya lo hace normalmente)
            for table in tables:
                self.db.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
                print(f"✓ AUTO_INCREMENT de {table} reiniciado")

            self.db.commit()
            print("✅ Base de datos limpiada exitosamente")
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error al limpiar la base de datos: {e}")
            raise
        finally:
            self.db.close()

