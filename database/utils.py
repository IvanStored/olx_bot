from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.database import db_session
from database.models import User, SearchParams, Favorite


class UserService:
    def __init__(self):
        self.db = db_session

    def create_user(
        self,
        username: str,
        price_from: int,
        price_to: int,
        state: str,
        gender: str,
        city: str,
    ) -> None:
        try:
            new_user = User(username=username)
            params = SearchParams(
                user=new_user,
                price_from=price_from,
                price_to=price_to,
                state=state,
                gender=gender,
                city=city,
            )
            self.db.add(new_user, params)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()

    def get_user_by_username(self, username: str) -> User:
        user = self.db.execute(
            select(User).where(User.username == username)  # noqa
        ).scalar_one_or_none()
        return user

    def update_user_settings(
        self,
        user: User,
        gender: str = None,
        city: str = None,
        price_from: str = None,
        price_to: str = None,
        state: str = None,
    ) -> None:
        if gender:
            user.search_params.gender = gender
        if city:
            user.search_params.city = city
        if price_from and price_to:
            user.search_params.price_from = price_from
            user.search_params.to = price_to
        if state:
            user.search_params.state = state
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()

    def add_to_favorite(
        self, username: str, name: str, price: str, date: str, link: str
    ) -> None | bool:
        bicycle = Favorite(
            name=name,
            price=price,
            date=date,
            link=link,
        )
        user = self.get_user_by_username(username=username)
        user.favorites.append(bicycle)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return False


user_service = UserService()
