import os
import sys
import transaction as ts

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_tm_session,
    get_session_factory,
    User
)
from ..models.product import Product


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)

    with ts.manager:
        dbsession = get_tm_session(session_factory, ts.manager)
        user = User()
        user.id = 'cece8926-2856-485e-8095-7c7a63f7997f'
        user.name = "John"
        user.surname = "Doe"
        user.email = "johndoe@example.com"
        dbsession.add(user)

        product1 = Product()
        product1.id = 'ae56f3bd-87d5-49a3-99e9-6156f8815741'
        product1.name = 'Axle'
        product1.description = 'The axle is responsible for transferring power from the engine to the wheels.'
        product1.price = 599.99
        dbsession.add(product1)

        product2 = Product()
        product2.id = '1f92f4d2-85e7-40b9-8b0b-72ebc03c57d4'
        product2.name = 'AC Compressor'
        product2.description = 'The AC compressor cycles through Freon in order to provide cool air throughout the vehicle.'
        product2.price = 1199.99
        dbsession.add(product2)

        product3 = Product()
        product3.id = '6c32e6ad-8b20-4211-b0c2-e552bd4663ed'
        product3.name = 'Transmission'
        product3.description = 'A transmission is a machine in a power transmission system, which provides controlled application of the power.'
        product3.price = 1999.99
        dbsession.add(product3)
