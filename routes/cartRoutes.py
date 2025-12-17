from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal
from controller import cartController
from schemas.cartSchemas import CartCreate, CartItemResponse
from schemas.userSchemas import User
from config.jwt import get_current_user

cart_router = APIRouter(prefix="/cart", tags=["cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_router.post("/add", response_model=CartItemResponse)
def add_to_cart_route(cart_data: CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = cartController.add_to_cart(db, current_user.id, cart_data.product_id, cart_data.quantity)
    if not item:
        raise HTTPException(status_code=400, detail="Product not available or insufficient stock")
    return item


@cart_router.get("/mycart", response_model=list[CartItemResponse])
def view_cart_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return cartController.get_cart(db, current_user.id)


@cart_router.delete("/remove/{product_id}")
def remove_from_cart_route(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = cartController.remove_from_cart(db, current_user.id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return item  # ya es un dict con "message"


@cart_router.post("/purchase")
def purchase_cart_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = cartController.purchase_cart(db, current_user.id)

    # Si realmente no hubo nada en purchased ni en skipped, entonces sí devolvemos error
    if not result["purchased"] and not result["skipped"]:
        raise HTTPException(status_code=400, detail="No products available for purchase")

    return {
        "message": "Purchase completed",
        "products": result
    }
