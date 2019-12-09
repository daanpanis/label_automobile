from sqlalchemy.orm import Session

from label_automobile.models.shopping_cart import ShoppingCartItem


class ShoppingCartRepository:
    def __init__(self, session: Session):
        self.session = session
        self.model = ShoppingCartItem

    def get_cart_items(self, user_id: str):
        return self.session.query(ShoppingCartItem).filter(ShoppingCartItem.user_id == user_id).all()

    def add_cart_item(self, user_id: str, product_id: str, amount: int):
        cart_item = ShoppingCartItem()
        cart_item.user_id = user_id
        cart_item.product_id = product_id
        cart_item.amount = amount
        self.session.add(cart_item)
        self.session.commit()

    def remove_cart_item(self, user_id: str, product_id: str):
        self.session.query(ShoppingCartItem).filter(
            ShoppingCartItem.user_id == user_id and ShoppingCartItem.product_id == product_id).delete()
        self.session.commit()
