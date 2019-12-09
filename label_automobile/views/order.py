from pyramid.httpexceptions import HTTPUnauthorized, HTTPNotFound, HTTPBadRequest
from pyramid.request import Request
from pyramid.view import view_defaults, view_config

from label_automobile.repositories.order import OrderRepository
from label_automobile.repositories.product import ProductRepository
from label_automobile.services.shopping_cart import ShoppingCartService
from datetime import datetime, date


@view_defaults(renderer='json')
class OrderView:
    def __init__(self, request: Request):
        self.request = request
        self.session = request.dbsession
        self.order_repository = OrderRepository(self.session)
        self.product_repository = ProductRepository(self.session)
        self.cart_service = ShoppingCartService(self.session)

    @view_config(route_name='order.list')
    def get_for_user(self):
        user = self.request.user
        if user is None:
            return HTTPUnauthorized()
        return [order.as_dict() for order in self.order_repository.find_by_user(user.id)]

    @view_config(route_name='order.details')
    def get_by_id(self):
        user = self.request.user
        order = self.order_repository.find_by_id(self.request.matchdict['id'])
        if user is None and (order is not None and order.user_id != user.id):
            return HTTPUnauthorized()
        elif order is None:
            return HTTPNotFound()
        return order.as_dict()

    @view_config(route_name='order.add')
    def add_order(self):
        user = self.request.user
        if user is None:
            return HTTPUnauthorized()
        cart = self.cart_service.get_cart(user.id)
        if cart is None or len(cart) == 0:
            return HTTPBadRequest(body='Shopping cart is empty')

        args = self.request.json_body
        missing = self._missing_args()
        if len(missing) > 0:
            return HTTPBadRequest(body='Missing arguments: ' + ','.join(missing))

        try:
            delivery_date = datetime.strptime(args['deliveryDate'], '%Y-%m-%d').date()
        except ValueError:
            return HTTPBadRequest(body='Delivery date must be formatted as year-month-day')

        if delivery_date is None or delivery_date <= date.today():
            return HTTPBadRequest(body='Delivery date must be after today')

        order = self.order_repository.add_order(user.id, args['address'], args['houseNumber'], args['postalCode'],
                                                delivery_date, [(item.product_id, item.amount) for item in cart])
        self.cart_service.clear_cart(user.id)
        return order.as_dict()

    def _missing_args(self) -> [str]:
        args = self.request.json_body
        missing = []
        required_args = ['address', 'houseNumber', 'postalCode', 'deliveryDate']
        for required_arg in required_args:
            if required_arg not in args or len(args[required_arg].strip()) == 0:
                missing.append(required_arg)
        return missing
