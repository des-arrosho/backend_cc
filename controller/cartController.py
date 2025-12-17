from sqlalchemy.orm import Session
from models.cartModel import Cart
from models.productsModel import Product
from models.purchaseModel import Purchase
from schemas.productSchemas import StatusProducto


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.status != StatusProducto.disponible.value:
        return None

    # Buscar si ya está en el carrito
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

    # Calcular la nueva cantidad total que quedaría en el carrito
    new_quantity = quantity + (cart_item.quantity if cart_item else 0)

    # Verificar stock real
    if new_quantity > product.quantity:
        return None  # Stock insuficiente

    # Actualizar o crear el carrito
    if cart_item:
        cart_item.quantity = new_quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    # Devuelve dict listo para Pydantic
    return {
        "product_id": product.id,
        "name": product.name,
        "price": product.price,
        "image_url": product.image_url,
        "quantity": cart_item.quantity
    }


def get_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    result = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            result.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "image_url": product.image_url,
                "quantity": item.quantity
            })
    return result


def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        return {"message": "El producto no está en el carrito"}

    db.delete(cart_item)
    db.commit()
    return {"message": f"Producto {product_id} eliminado del carrito"}


def purchase_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    purchased = []
    skipped = []

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            skipped.append({"product_id": item.product_id, "reason": "Producto no existe"})
            db.delete(item)
            continue

        if product.created_by == user_id:
            skipped.append({"product_id": product.id, "reason": "Producto propio"})
            db.delete(item)
            continue

        if product.status != StatusProducto.disponible.value:
            skipped.append({"product_id": product.id, "reason": "Producto no disponible"})
            db.delete(item)
            continue

        if product.quantity >= item.quantity:
            # Reducir stock
            product.quantity -= item.quantity
            if product.quantity == 0:
                product.status = StatusProducto.agotado.value

            # Crear registro de Purchase
            total_price = product.price * item.quantity
            purchase = Purchase(
                user_id=user_id,
                product_id=product.id,
                quantity=item.quantity,
                total_price=total_price
            )
            db.add(purchase)

            # Preparar respuesta lista para Pydantic
            purchased.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "total_price": total_price,
                "image_url": product.image_url
            })

            db.delete(item)  # Limpiar carrito
        else:
            skipped.append({"product_id": product.id, "reason": "Stock insuficiente"})

    db.commit()
    return {"purchased": purchased, "skipped": skipped}
