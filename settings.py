import os
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
from redis.asyncio.client import Redis

load_dotenv()


class Config:
    storage = Redis(
        host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT"))
    )
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('PG_HOST')}:{int(os.getenv('PG_PORT'))}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOMAIN = "https://www.olx.ua"

    PAGES_COUNT = 1
    BICYCLE_URL = DOMAIN + "/d/uk/hobbi-otdyh-i-sport/velo/velosipedy/"
    CITIES = {"Херсон": "kherson", "Киев": "kiev", "Одесса": "odessa"}
    STAN = {"Б/У": "used", "Новые": "new", "Все": "Oba"}
    GENDER = {
        "Для мужчин": "for_men",
        "Для женщин": "for_women",
        "Для подростков": "for_teenagers",
        "Универсальные": "universal",
    }


class SearchParameters(StatesGroup):
    price_diapazon = State()
    price_from = State()
    price_to = State()
    city = State()
    stan = State()
    gender = State()
