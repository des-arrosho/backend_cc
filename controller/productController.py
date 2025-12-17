# controller/productController.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.productsModel import Product
from schemas.productSchemas import ProductCreate
from fastapi import HTTPException

def create_product(db: Session, product_data: dict):
    try:
        db_product = Product(**product_data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

def get_products(db: Session):
    try:
        products = db.query(Product).all()
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_product(db: Session, product_id: int):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def update_product(db: Session, product_id: int, updates: dict):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Product not found")

        # Actualizar campos usando dict
        for field, value in updates.items():
            setattr(db_product, field, value)

        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")


def delete_product(db: Session, product_id: int):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(db_product)
        db.commit()
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")
