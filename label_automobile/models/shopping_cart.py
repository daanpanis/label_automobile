from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from label_automobile.models.meta import Base, BaseModel


class ShoppingCartItem(BaseModel, Base):
    __tablename__ = 'shopping_cart_item'

    user_id = Column('user_id', ForeignKey('user.id'), primary_key=True)
    product_id = Column('product_id', ForeignKey('product.id'), primary_key=True)
    _amount = Column(Integer, nullable=False)

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
