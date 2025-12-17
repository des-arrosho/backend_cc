import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from models.purchaseModel import Purchase

# -------------------------
# 1. Cargar datos desde DB
# -------------------------
def load_purchases(db):
    purchases = db.query(Purchase).all()
    data = [
        {
            "user_id": p.user_id,
            "product_id": p.product_id,
            "quantity": p.quantity,
            "total_price": p.total_price,
            "created_at": p.created_at
        }
        for p in purchases
    ]
    return pd.DataFrame(data)

# -------------------------
# 2. Crear dataset supervisado
# -------------------------
def build_dataset(purchase_df):
    purchase_df = purchase_df.copy()
    purchase_df["label"] = 1

    users = purchase_df["user_id"].unique()
    products = purchase_df["product_id"].unique()

    # Crear ejemplos negativos realistas
    negative_samples = []
    for user in users:
        purchased_products = purchase_df[purchase_df.user_id == user]["product_id"].tolist()
        not_purchased = [p for p in products if p not in purchased_products]
        for p in not_purchased:
            negative_samples.append({
                "user_id": user,
                "product_id": p,
                "quantity": 0,
                "total_price": 0.0,
                "label": 0
            })

    neg_df = pd.DataFrame(negative_samples)
    final_df = pd.concat([purchase_df, neg_df], ignore_index=True)

    # Guardar dataset final en CSV
    final_df.to_csv("purchase_dataset.csv", index=False)

    return final_df

# -------------------------
# 3. Entrenar modelo
# -------------------------
def train_model(df):
    X = df[["user_id", "product_id", "quantity", "total_price"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=42)
    model.fit(X_train, y_train)

    # Predicciones para guardar en CSV
    df_pred = X_test.copy()
    df_pred["true_label"] = y_test
    df_pred["pred_label"] = model.predict(X_test)
    df_pred.to_csv("purchase_predictions.csv", index=False)

    # Evaluación
    y_pred = df_pred["pred_label"]
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)

    return model, report, cm, acc
