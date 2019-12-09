from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from label_automobile.models.meta import Base, BaseModel


class User(BaseModel, Base):
    __tablename__ = 'user'

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email_ = Column(String, nullable=False, unique=True, name='email')
    password = Column(String)

    active = Column(Boolean, nullable=False, default=False)

    @hybrid_property
    def email(self):
        return self.email_

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise Exception('Invalid Email')
        self.email_ = value

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name,
            'surname': self.surname,
            'email': self.email
        }
