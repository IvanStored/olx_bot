from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    search_params = relationship(
        "SearchParams", back_populates="user", uselist=False
    )
    favorites = relationship(
        "Favorite",
        secondary="user_favorite",
        back_populates="users",
    )


class SearchParams(Base):
    __tablename__ = "search_params"
    id = Column(Integer, primary_key=True)
    user_username = Column(String(32), ForeignKey("users.username"))
    user = relationship("User", back_populates="search_params", uselist=False)
    price_from = Column(Integer, nullable=False)
    price_to = Column(Integer, nullable=False)
    state = Column(String(5), nullable=False)
    gender = Column(String(13), nullable=False)
    city = Column(String(32), nullable=False)


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    users = relationship(
        "User",
        secondary="user_favorite",
        back_populates="favorites",
    )
    name = Column(String(200), nullable=False)
    price = Column(String(40), nullable=False)
    date = Column(String(200), nullable=False)
    link = Column(String(200), nullable=False, unique=True)


class UserFavorite(Base):
    __tablename__ = "user_favorite"
    user_username = Column(
        String(32), ForeignKey("users.username"), primary_key=True
    )
    favorite_link = Column(
        String(200), ForeignKey("favorites.link"), primary_key=True
    )
