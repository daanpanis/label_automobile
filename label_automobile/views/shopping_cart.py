from pyramid.httpexceptions import HTTPUnauthorized, HTTPOk, HTTPNotFound
from pyramid.request import Request
from pyramid.view import view_config, view_defaults

from label_automobile.repositories.product import ProductRepository
from label_automobile.services.shopping_cart import ShoppingCartService


@view_defaults(renderer='json')
class ShoppingCartView:
    def __init__(self, request: Request):
        self.request = request
        self.session = request.dbsession
        self.shopping_cart_service = ShoppingCartService(self.session)
        self.product_repository = ProductRepository(self.session)

    @view_config(route_name='shopping_cart.cart')
    def get_cart(self):
        user = self.request.user
        if user is None:
            return HTTPUnauthorized()

        return [item.as_dict() for item in self.shopping_cart_service.get_cart(user.id)]

    @view_config(route_name='shopping_cart.add_one')
    def add_one(self):
        user = self.request.user
        if user is None:
            return HTTPUnauthorized()
        product = self.product_repository.find_by_id(self.request.matchdict['id'])
        if product is None:
            return HTTPNotFound()
        self.shopping_cart_service.add_one(user.id, product.id)
        return HTTPOk(body='')

    @view_config(route_name='shopping_cart.remove_one')
    def remove_one(self):
        user = self.request.user
        if user is None:
            return HTTPUnauthorized()
        product = self.product_repository.find_by_id(self.request.matchdict['id'])
        if product is None:
            return HTTPNotFound()
        self.shopping_cart_service.remove_one(user.id, product.id)
        return HTTPOk(body='')

    @view_config(route_name='shopping_cart.remove_all')
    def remove_all(self):
        user = self.request.user
        if user is None:
            return HTTPUnauthorized()
        product = self.product_repository.find_by_id(self.request.matchdict['id'])
        if product is None:
            return HTTPNotFound()
        self.shopping_cart_service.remove_all(user.id, product.id)
        return HTTPOk(body='')
