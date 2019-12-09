from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from label_automobile.models.meta import Base, BaseModel


class Product(BaseModel, Base):
    __tablename__ = 'product'

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(DECIMAL(scale=2), nullable=False)

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name,
            'description': self.description,
            'price': self.price.__float__()
        }
