from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from label_automobile.models.meta import BaseModel, Base


class Order(BaseModel, Base):
    __tablename__ = 'order'

    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_item'

    order_id = Column(String, ForeignKey('order.id'), primary_key=True)
    order = relationship('Order', back_populates='items')

    product_id = Column(String, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')

    _amount = Column(Integer, nullable=False, default=1)

    @hybrid_property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            raise Exception('Amount not a number')
        elif value <= 0:
            raise Exception('Amount must be at least 1')
        self._amount = value
