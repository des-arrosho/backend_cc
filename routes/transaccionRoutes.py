from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.productsModel import Product
from models.usersModel import User
from config.jwt import get_current_user
from schemas.transactionSchemas import BuyRequest


transaction_router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@transaction_router.post("/buy")
def buy_product(
    data: BuyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if product.created_by == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes comprar tus propios productos")

    if product.quantity < data.quantity:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible")

    product.quantity -= data.quantity
    if product.quantity == 0:
        product.status = "agotado"

    db.commit()
    db.refresh(product)

    return {
        "message": "Compra realizada con éxito",
        "producto": product.name,
        "restante": product.quantity
    }