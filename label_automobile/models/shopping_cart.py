from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from label_automobile.models.meta import Base


class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_item'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')
    _amount = Column(Integer, nullable=False, name="amount")

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

    def as_dict(self):
        return {
            'product': self.product.as_dict() if self.product is not None else {
                'id': self.product_id.__str__()
            },
            'amount': self._amount
        }
