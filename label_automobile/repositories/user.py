from sqlalchemy.orm import Session

from label_automobile.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).one_or_none()

    def find_by_email(self, email):
        return self.session.query(User).filter(
            User.email == email).one_or_none()
