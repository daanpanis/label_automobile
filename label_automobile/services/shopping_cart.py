from sqlalchemy.orm import Session

from label_automobile.models.shopping_cart import ShoppingCartItem
from label_automobile.repositories.shopping_cart import ShoppingCartRepository


class ShoppingCartService:
    def __init__(self, session: Session):
        self._repository = ShoppingCartRepository(session)

    def add_one(self, user_id, product_id):
        print(product_id)
        cart_item = self._repository.get_cart_item(user_id, product_id)
        if cart_item is None:
            self._repository.add_cart_item(user_id, product_id, 1)
        else:
            self._repository.update_cart_item(user_id, cart_item.product_id, cart_item.amount + 1)

    def remove_one(self, user_id, product_id):
        cart_item = self._repository.get_cart_item(user_id, product_id)
        if cart_item is None:
            return

        if cart_item.amount > 1:
            self._repository.update_cart_item(user_id, product_id, cart_item.amount - 1)
        else:
            self._repository.remove_cart_item(user_id, product_id)

    def remove_all(self, user_id, product_id):
        self._repository.remove_cart_item(user_id, product_id)

    def clear_cart(self, user_id):
        self._repository.clear_cart(user_id)

    def get_cart(self, user_id) -> [ShoppingCartItem]:
        return self._repository.get_cart_items(user_id)
