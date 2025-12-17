from sqlalchemy.orm import Session
from services.trainingSp import load_purchases, build_dataset, train_model
import pandas as pd

def train_purchase_model(db: Session):
    df = load_purchases(db)
    if df.empty:
        return None, "No hay compras registradas", None, None, None
    
    dataset = build_dataset(df)
    model, report, cm, acc = train_model(dataset)
    return model, "Modelo entrenado", report, cm, acc

def get_ml_dashboard_data(db: Session):
    df = load_purchases(db)
    if df.empty:
        return {"message": "No hay compras registradas"}

    dataset = build_dataset(df)
    model, report, cm, acc = train_model(dataset)

    # Predicciones
    X = dataset[["user_id","product_id","quantity","total_price"]]
    dataset["pred_label"] = model.predict(X)
    dataset["pred_prob"] = model.predict_proba(X)[:,1]

    # Productos más vistos (basado en compras reales)
    top_products = df.groupby("product_id").size().reset_index(name="visitas").sort_values(by="visitas", ascending=False).head(10)

    # Evolución del consumo responsable por mes
    df["mes"] = pd.to_datetime(df["created_at"]).dt.to_period("M").astype(str)
    consumo_data = df.groupby("mes")["total_price"].sum().reset_index(name="score")

    # Probabilidad de compra por producto
    product_summary = dataset.groupby("product_id")["pred_prob"].mean().reset_index()
    product_summary.rename(columns={"pred_prob":"probabilidad_compra"}, inplace=True)

    # Compras probables por usuario
    user_summary = dataset.groupby("user_id")["pred_label"].sum().reset_index()
    user_summary.rename(columns={"pred_label":"compras_probables"}, inplace=True)

    return {
        "accuracy": acc,
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "top_products": top_products.to_dict(orient="records"),
        "consumo_data": consumo_data.to_dict(orient="records"),
        "product_summary": product_summary.to_dict(orient="records"),
        "user_summary": user_summary.to_dict(orient="records")
    }
