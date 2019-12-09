from datetime import date
from typing import Tuple

from sqlalchemy.orm import Session

from label_automobile.models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_order(self, user_id, address: str, house_number: str, postal_code: str, delivery_date: date,
                  items: [Tuple[str, int]]) -> Order:
        order = Order()
        order.user_id = user_id
        order.address = address
        order.house_number = house_number
        order.postal_code = postal_code
        order.delivery_date = delivery_date
        order.items = []

        for item in items:
            order_item = OrderItem()
            order_item.order_id = order.id,
            order_item.product_id = item[0]
            order_item.amount = item[1]
            order.items.append(order_item)

        self.session.add(order)
        return order

    def find_by_id(self, order_id) -> Order:
        return self.session.query(Order).filter(Order.id == order_id).one_or_none()

    def find_by_user(self, user_id) -> [Order]:
        return self.session.query(Order).filter(Order.user_id == user_id).all()
