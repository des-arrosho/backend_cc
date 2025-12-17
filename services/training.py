from sqlalchemy.orm import Session
from models.interactionModel import Interaccion
from models.productsModel import Product
from schemas.productSchemas import StatusProducto
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def entrenar_recomendaciones(db, user_id):
    # 1. Obtener interacciones del usuario
    interacciones = db.query(Interaccion).filter(Interaccion.user_id == user_id).all()
    if not interacciones:
        return []

    productos_ids = [i.product_id for i in interacciones]

    todos_productos = db.query(Product).filter(
        Product.status == StatusProducto.disponible.value,
        Product.quantity > 0
    ).all()
    if not todos_productos:
        return []

    df = pd.DataFrame([{
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "price": p.price,
        "quantity": p.quantity,
        "status": p.status,
        "carbon_footprint": p.carbon_footprint,
        "recyclable_packaging": int(p.recyclable_packaging),
        "local_origin": int(p.local_origin)
    } for p in todos_productos])

    df["text"] = (
        df["category"] + " " +
        df["recyclable_packaging"].astype(str) + " " +
        df["local_origin"].astype(str)
    )

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["text"])

    n_clusters = min(5, len(df))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(tfidf_matrix)

    sil_score = silhouette_score(tfidf_matrix, df["cluster"]) if len(df) > 1 else 0.0

    vistos_idx = df[df["id"].isin(productos_ids)].index
    if vistos_idx.empty:
        return []

    similarity_scores = cosine_similarity(tfidf_matrix[vistos_idx], tfidf_matrix)
    avg_scores = similarity_scores.mean(axis=0)

    max_footprint = df["carbon_footprint"].max()
    min_footprint = df["carbon_footprint"].min()
    df["carbon_score"] = 1 - (df["carbon_footprint"] - min_footprint) / (max_footprint - min_footprint + 1e-6)

    max_price = df["price"].max()
    min_price = df["price"].min()
    df["price_score"] = 1 - (df["price"] - min_price) / (max_price - min_price + 1e-6)

    df["sustentabilidad_score"] = (df["carbon_score"] + df["recyclable_packaging"] + df["local_origin"]) / 3
    df["score"] = 0.5 * avg_scores + 0.3 * df["sustentabilidad_score"] + 0.2 * df["price_score"]

    recomendados = df[~df["id"].isin(productos_ids)].sort_values("score", ascending=False)

    # Guardar CSV de todos los productos
    df.to_csv("all_products.csv", index=False)

    # Guardar CSV de recomendaciones finales
    recomendados.head(5).to_csv(f"recomendaciones_usuario_{user_id}.csv", index=False)

    return {
        "silhouette_score": sil_score,
        "clusters": df[["id", "name", "cluster"]].to_dict(orient="records"),
        "recomendaciones": recomendados.head(5).to_dict(orient="records")
    }
