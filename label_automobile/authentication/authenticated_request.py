from pyramid.request import Request

from label_automobile.services.user import UserService


# A very basic authentication implementation.
# It looks for the 'Authorization' header in the request and tries to resolve a user using the value of the header.
# This obviously is a very insecure authentication since no login is required, you only need to know someone's user id.
def get_user(request: Request):
    for key in request.headers.keys():
        print(key)
    user_id = request.headers.get('Authorization')
    if user_id is None:
        return None

    return UserService(request.dbsession).find_by_id(user_id)
