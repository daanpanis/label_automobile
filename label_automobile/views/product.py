from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request
from pyramid.view import view_defaults, view_config

from label_automobile.repositories.product import ProductRepository


@view_defaults(renderer='json')
class ProductView:
    def __init__(self, request: Request):
        self.request = request
        self.session = request.dbsession
        self.product_repository = ProductRepository(self.session)

    @view_config(route_name='product.list')
    def list(self):
        return self.product_repository.find_all()

    @view_config(route_name='product.details')
    def details(self, product_id: str):
        product = self.product_repository.find_by_id(product_id)
        if product is None:
            return HTTPNotFound()
        return product
