from sqlalchemy.orm import Session
from config.db import SessionLocal
from passlib.context import CryptContext
from faker import Faker
import random
from datetime import datetime, timedelta
from models.usersModel import User
from models.productsModel import Product
from models.interactionModel import Interaccion
from models.commentModel import Comment
from models.cartModel import Cart
from schemas.productSchemas import StatusProducto
from models.purchaseModel import Purchase
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Seeder:
    def __init__(self):
        self.db = SessionLocal()
        self.faker = Faker("es_ES")
        self.batch_size = 200

        # Diccionario de productos ecológicos
        self.PRODUCTOS_POR_CATEGORIA = {
            "Alimentos": {
                "productos": [
                    "Pan integral", "Leche de almendras", "Miel pura", "Chocolate negro",
                    "Café", "Galletas de avena", "Aceite de oliva", "Quinoa",
                    "Pasta de trigo duro"
                ],
                "materiales": ["orgánico", "vegano", "artesanal"],
                "carbon_footprint_range": (0.5, 5.0),
                "sufijos": ["(Pack familiar)", "(Sin aditivos)", "(Energético)"]
            },
            "Ropa": {
                "productos": [
                    "Camiseta básica", "Pantalón", "Vestido largo", "Chaqueta",
                    "Calcetines", "Bragas térmicas", "Jersey", "Sombrero"
                ],
                "materiales": ["algodón orgánico", "bambú", "lino reciclado", "Piel"],
                "carbon_footprint_range": (5.0, 25.0),
                "sufijos": ["(Edición limitada)", "(Talla ética)", "(Pack 3 u.)"]
            },
            "Limpieza": {
                "productos": [
                    "Jabón", "Detergente en pastilla", "Limpiador multiusos", "Suavizante",
                    "Desinfectante natural", "Esponja vegetal", "Cepillo de madera", "Bolsa de lavado"
                ],
                "materiales": ["biodegradable", "orgánico", "Sin quimicos"],
                "carbon_footprint_range": (1.0, 8.0),
                "sufijos": ["(Zero waste)", "(Sin fragancia)", "(Concentrado)"]
            },
            "Tecnologia": {
                "productos": [
                    "Cargador solar", "Auriculares inalámbricos", "Power bank", "Fundas para móvil",
                    "Tablet", "Teclado ergonómico", "Ratón de bambú", "Altavoz portátil"
                ],
                "materiales": ["energía solar", "plástico reciclado", "metales reciclados"],
                "carbon_footprint_range": (10.0, 50.0),
                "sufijos": ["(Eficiencia A+)", "(Reparable)", "(Modular)"]
            },
            "Hogar": {
                "productos": ["Vela aromática", "Taza", "Tabla de cortar", "Repisa"],
                "materiales": ["cera", "plastico reciclado"],
                "carbon_footprint_range": (3.0, 20.0),
                "sufijos": ["(Hecho a mano)", "(Diseño circular)"]
            },
            "Salud": {
                "productos": [
                    "Crema facial", "Protector solar", "Aceite para masaje", "Jabón íntimo",
                    "Suplemento vitamínico", "Desodorante ", "Cepillo de dientes", "Hilo dental"
                ],
                "materiales": ["a base de ingredientes naturales", "sin quimicos", "orgánico"],
                "carbon_footprint_range": (2.0, 12.0),
                "sufijos": ["(Dermatológico)", "(Sin fragancia)"]
            },
            "Papeleria": {
                "productos": [
                    "Cuaderno anillado", "Bolígrafo recargable", "Carpeta archivador", "Sobre kraft",
                    "Postales ilustradas", "Bloc de notas", "Agenda anual", "Lápices de colores"
                ],
                "materiales": ["papel semilla", "cartón reciclado", "tinta vegetal"],
                "carbon_footprint_range": (1.5, 6.0),
                "sufijos": ["(Plantable)", "(100% reciclado)"]
            },
            "Otro": {
                "productos": [
                    "Kit de jardinería", "Juego de cubiertos", "Decoración mural", "Caja regalo",
                    "Bolsa de tela", "Velas decorativas", "Portalápices", "Reloj de pared"
                ],
                "materiales": ["upcycled", "hecho a mano", "materiales mixtos"],
                "carbon_footprint_range": (2.0, 15.0),
                "sufijos": ["(Multiusos)", "(Personalizable)"]
            },
        }

    def generar_producto_ecologico(self, user_ids):
        categoria = random.choice(list(self.PRODUCTOS_POR_CATEGORIA.keys()))
        datos = self.PRODUCTOS_POR_CATEGORIA[categoria]
        nombre = f"{random.choice(datos['productos'])} de {random.choice(datos['materiales'])} {random.choice(datos['sufijos'])}"
        carbon_footprint = round(random.uniform(*datos["carbon_footprint_range"]), 2)

        # Status aleatorio entre disponible y agotado (más probabilidad disponible)
        status = random.choices(
            [StatusProducto.disponible.value, StatusProducto.agotado.value],
            weights=[0.8, 0.2],
            k=1,
        )[0]

        return Product(
            name=nombre[:255],
            category=categoria[:100],
            carbon_footprint=carbon_footprint,
            recyclable_packaging=random.random() > 0.3,
            local_origin=random.random() > 0.6,
            image_url=f"https://res.cloudinary.com/dkerhtvlk/image/upload/v1753410633/productDefault_bddwkj.jpg{categoria.lower()}/{random.randint(1,50)}.jpg"[:500],
            price=round(random.uniform(5.0, 200.0), 2),
            quantity=random.randint(1, 100),
            status=status,
            created_by=random.choice(user_ids),
        )

    def run(self, total_records=1240):
        try:
            num_users = 150
            num_products = 190
            num_comments = 90
            num_interactions = 500
            num_carts = 200
            num_purchases = 110

            # 1. Usuarios
            print(f"🔹 Creando {num_users} usuarios...")
            for i in range(0, num_users, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_users - i)):
                    gender = random.choice(["male", "female"])
                    first_name = (
                        self.faker.first_name_male()
                        if gender == "male"
                        else self.faker.first_name_female()
                    )

                    batch.append(
                        User(
                            username=f"{first_name.lower()}{random.randint(10,99)}"[:50],
                            email=f"{first_name.lower()}.{self.faker.last_name().lower()}@gmail.com"[
                                :100
                            ],
                            password=self.hash_password("123456"),
                            profile_picture=f"https://randomuser.me/api/portraits/{'men' if gender == 'male' else 'women'}/{random.randint(1,99)}.jpg"[
                                :255
                            ],
                            status="active" if random.random() > 0.3 else "inactive",
                            registration_date=datetime.now()
                            - timedelta(days=random.randint(0, 365)),
                        )
                    )
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Usuarios {i+1}-{i+len(batch)} creados")

            # Obtener IDs de usuarios
            user_ids = [id[0] for id in self.db.query(User.id).yield_per(1000)]

            # 2. Productos
            print(f"\n🔹 Creando {num_products} productos...")
            for i in range(0, num_products, self.batch_size):
                batch = [
                    self.generar_producto_ecologico(user_ids)
                    for _ in range(min(self.batch_size, num_products - i))
                ]
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Productos {i+1}-{i+len(batch)} creados")

            # Obtener productos y sus IDs
            products = self.db.query(Product).all()
            product_ids = [p.id for p in products]

            # 3. Comentarios
            print(f"\n🔹 Creando {num_comments} comentarios...")
            opiniones = [
            "Excelente producto, muy recomendable.",
            "Me encantó, volvería a comprarlo.",
            "Buena relación calidad-precio.",
            "No era lo que esperaba, pero funciona.",
            "Empaque ecológico, muy bien.",
            "Lo recibí a tiempo y en buen estado.",
            "Podría mejorar, pero cumple su función.",
            "Estoy satisfecho con la compra.",
            "Muy útil para reducir mi consumo de plástico.",
            "El empaque es completamente reciclable, me encanta.",
            "Buena iniciativa, excelente para el planeta.",
            "Materiales de muy buena calidad y ecológicos.",
            "Me gusta apoyar marcas conscientes.",
            "Funciona igual que uno convencional pero sin dañar el ambiente.",
            "Ideal para regalar a alguien que se preocupa por el medio ambiente.",
            "Producto natural, sin químicos innecesarios.",
            "Muy buena opción para quienes buscan alternativas sustentables.",
            "Recomiendo 100%, vale la pena cambiar a esto.",
            "Perfecto para quienes buscan alternativas sostenibles.",
            "El producto llegó en empaques reciclables, muy bien.",
            "Increíble lo cómodo y ecológico que es.",
            "Cumple su función sin generar residuos.",
            "Una excelente forma de aportar al medio ambiente.",
            "Ya es parte de mi día a día, muy útil.",
            "Lo volvería a comprar sin dudarlo.",
            "Es suave, duradero y sobre todo ecológico.",
            "Me ayudó a reducir mi basura en casa.",
            "Ideal para hogares sostenibles.",
            "Ayuda a reducir la huella de carbono.",
            "Fácil de usar y muy eficiente.",
            "Recomendado para familias que reciclan.",
            "Un producto responsable con el planeta.",
            "Me encanta su diseño natural.",
            "No pensé que funcionara tan bien siendo ecológico.",
            "Definitivamente voy a seguir comprando esta marca.",
            "Aporta a mi estilo de vida consciente.",
            "Funciona mejor que muchos productos industriales.",
            "Me sorprendió la calidad y su impacto positivo.",
            "Mis hijos también lo usan, es muy seguro.",
            "Una gran inversión para el futuro.",
            "Se siente bien saber que consumo responsablemente.",
            "Sustituí el producto anterior por este y no me arrepiento.",
            "Lo uso todos los días y no se desgasta.",
            "Gran relación calidad-precio y eco-friendly.",
            "La textura natural es increíble.",
            "Mis amigos también lo compraron tras probarlo.",
            "Huele delicioso y es 100% natural.",
            "Nunca había encontrado algo tan ecológico y útil."
            ]
            for i in range(0, num_comments, self.batch_size):
                batch = [
                    Comment(
                        user_id=random.choice(user_ids),
                        product_id=random.choice(product_ids),
                        content=random.choice(opiniones)[:500],
                    )
                    for _ in range(min(self.batch_size, num_comments - i))
                ]
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Comentarios {i+1}-{i+len(batch)} creados")

            # 4. Interacciones
            print(f"\n🔹 Creando {num_interactions} interacciones...")
            for i in range(0, num_interactions, self.batch_size):
                batch = [
                    Interaccion(
                        user_id=random.choice(user_ids),
                        product_id=random.choice(product_ids),
                        interaction=random.randint(1, 3),
                    )
                    for _ in range(min(self.batch_size, num_interactions - i))
                ]
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Interacciones {i+1}-{i+len(batch)} creados")

            # 5. Carritos
            print(f"\n🔹 Creando {num_carts} carritos...")
            valid_products = [p for p in products if p.status != StatusProducto.agotado.value]

            for i in range(0, num_carts, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_carts - i)):
                    user_id = random.choice(user_ids)
                    product = random.choice(valid_products)

                    # evitar que un usuario compre su propio producto
                    while product.created_by == user_id:
                        product = random.choice(valid_products)

                    batch.append(
                        Cart(
                            user_id=user_id,
                            product_id=product.id,
                            quantity=random.randint(1, 5),
                        )
                    )

                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Carritos {i+1}-{i+len(batch)} creados")
                
            # 6. Purcharse
            print(f"\n🔹 Creando compras desde carritos...")
            
            # Trae todos los carritos ya creados
            carts = self.db.query(Cart).options(joinedload(Cart.product)).all()
            random.shuffle(carts)
            purchases_batch = []
            
            existing_purchases = set(
                (p.user_id, p.product_id) for p in self.db.query(Purchase.user_id, Purchase.product_id).all()
            )

            for cart in carts[:num_purchases]:
                key = (cart.user_id, cart.product_id)
                
                if key not in existing_purchases and cart.product:
                    purchase = Purchase(
                        user_id=cart.user_id,
                        product_id=cart.product_id,
                        quantity=cart.quantity,
                        total_price=cart.quantity * cart.product.price,
                )
                purchases_batch.append(purchase)
                existing_purchases.add(key)  # Marcar como creada
                self.db.delete(cart)
                
                self.db.add_all(purchases_batch)
                self.db.commit()
            
            print(f"Compras creadas: {len(purchases_batch)}")
            

            print(f"\n🎉 Seeder completado exitosamente!")
            print(
                f"Total registros creados: {num_users + num_products + num_comments + num_interactions + num_carts + num_purchases}"
            )

        except Exception as e:
            self.db.rollback()
            print(f"\n❌ Error crítico: {str(e)}")
            raise
        finally:
            self.db.close()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
