from sqlalchemy import String, ForeignKey, Column, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from label_automobile.models.meta import BaseModel, Base


class Order(BaseModel, Base):
    __tablename__ = 'order'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    items = relationship('OrderItem')
    address = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    delivery_date = Column(Date, nullable=False)

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'user': self.user.as_dict() if self.user is not None else {
                'id': self.user_id.__str__()
            },
            'items': [item.as_dict() for item in self.items] if self.items is not None else [],
            'address': self.address,
            'houseNumber': self.house_number,
            'postalCode': self.postal_code,
            'deliveryDate': self.delivery_date.strftime('%Y-%m-%d')
        }


class OrderItem(Base):
    __tablename__ = 'order_item'

    order_id = Column(UUID(as_uuid=True), ForeignKey('order.id'), primary_key=True)

    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')

    _amount = Column(Integer, nullable=False, default=1, name="amount")

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
            'amount': self.amount
        }
