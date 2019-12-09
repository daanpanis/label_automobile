from sqlalchemy.orm import Session

from label_automobile.models.shopping_cart import ShoppingCartItem


class ShoppingCartRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_cart_items(self, user_id):
        return self.session.query(ShoppingCartItem).filter(ShoppingCartItem.user_id == user_id).all()

    def get_cart_item(self, user_id, product_id) -> ShoppingCartItem:
        return self._query_item(user_id, product_id).one_or_none()

    def add_cart_item(self, user_id, product_id, amount: int) -> ShoppingCartItem:
        cart_item = ShoppingCartItem()
        cart_item.user_id = user_id
        cart_item.product_id = product_id
        cart_item.amount = amount
        self.session.add(cart_item)
        return cart_item

    def remove_cart_item(self, user_id, product_id):
        self._query_item(user_id, product_id).delete()

    def update_cart_item(self, user_id, product_id, amount: int):
        self._query_item(user_id, product_id).update({'amount': amount})

    def clear_cart(self, user_id):
        self.session.query(ShoppingCartItem).filter(ShoppingCartItem.user_id == user_id).delete()

    def _query_item(self, user_id, product_id):
        return self.session.query(ShoppingCartItem).filter(ShoppingCartItem.user_id == user_id).filter(
            ShoppingCartItem.product_id == product_id)
