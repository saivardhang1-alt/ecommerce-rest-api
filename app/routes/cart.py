from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CartItem, Product
from app.schemas import CartItemCreate, CartItemResponse

router = APIRouter(
    prefix="/cart",
    tags=["Shopping Cart"]
)


@router.post("/{user_id}", response_model=CartItemResponse)
def add_to_cart(
    user_id: int,
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if item.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    if product.stock < item.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        if product.stock < cart_item.quantity + item.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient product stock"
            )
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.get("/{user_id}", response_model=list[CartItemResponse])
def view_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).all()
