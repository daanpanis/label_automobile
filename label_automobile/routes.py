from label_automobile.authentication.authenticated_request import get_user


def includeme(config):
    config.add_request_method(get_user, 'user', reify=True)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('user.list', '/user', request_method="GET")
    config.add_route('user.find_by_email', '/user/email', request_method="GET")

    config.add_route('product.list', '/products', request_method='GET')
    config.add_route('product.details', '/products/{id}', request_method='GET')

    config.add_route('shopping_cart.cart', '/cart', request_method='GET')
    config.add_route('shopping_cart.add_one', '/cart/{id}', request_method=['POST', 'PUT'])
    config.add_route('shopping_cart.remove_one', '/cart/{id}', request_method='DELETE')
    config.add_route('shopping_cart.remove_all', '/cart/{id}/all', request_method='DELETE')

    config.add_route('order.list', '/orders', request_method='GET')
    config.add_route('order.details', '/orders/{id}', request_method='GET')
    config.add_route('order.add', '/orders', request_method=['POST', 'PUT'])
