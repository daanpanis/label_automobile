from sqlalchemy.orm import Session

from label_automobile.models.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> [Product]:
        return self.session.query(Product).all()

    def find_by_id(self, product_id: str) -> Product:
        return self.session.query(Product).filter(Product.id == product_id).one_or_none()
