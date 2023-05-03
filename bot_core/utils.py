import re

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def price_from_to(range_price: str) -> tuple:
    price_from, price_to = range_price.split(sep="-")
    return price_from, price_to


def validate_price_range(_range: str) -> bool | tuple:
    """

    :rtype: object
    """
    pattern = r"^\d+-+\d+$"
    match = re.match(pattern=pattern, string=_range)
    if not match:
        return False

    price_from, price_to = price_from_to(range_price=_range)
    if int(price_from) > int(price_to):
        return False
    return True


def make_keyboard(
    page: int, pages_count: int, favorite: bool = False
) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1
    left_button = InlineKeyboardButton("←", callback_data=f"to {left}")
    page_button = InlineKeyboardButton(
        f"{str(page)}/{str(pages_count)}", callback_data="_"
    )
    right_button = InlineKeyboardButton("→", callback_data=f"to {right}")
    add_to_favorite = InlineKeyboardButton(
        "Добавить в избранное", callback_data="add_to_favorite"
    )
    if favorite:
        left_button = InlineKeyboardButton("←", callback_data=f"fto {left}")
        page_button = InlineKeyboardButton(
            f"{str(page)}/{str(pages_count)}", callback_data="_"
        )
        right_button = InlineKeyboardButton("→", callback_data=f"fto {right}")
        buttons.add(left_button, page_button, right_button)
        return buttons
    buttons.add(left_button, page_button, right_button)
    buttons.add(add_to_favorite)
    return buttons


def make_message_text(
    page: int,
    favorites: list = None,
    result: dict = None,
) -> str:
    if favorites:
        bicycle = favorites[page - 1]
        return (
            f"{bicycle.name}\n{bicycle.price}\n{bicycle.date}\n{bicycle.link}"
        )

    bicycle = list(result.keys())[page - 1]

    return f"{result[bicycle]['bicycle']}\n{result[bicycle]['price']}\n{result[bicycle]['date']}\n{result[bicycle]['link']}"


def settings_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    gender = InlineKeyboardButton(
        "Поменять тип велосипеда", callback_data="gender"
    )
    city = InlineKeyboardButton("Поменять город", callback_data="city")
    price = InlineKeyboardButton(
        "Поменять диапазон цен", callback_data="price"
    )
    state = InlineKeyboardButton("Поменять состояние", callback_data="stan")
    favorite = InlineKeyboardButton("Избранное", callback_data="favorite")
    keyboard.add(gender, city, price, state, favorite)
    return keyboard


def check_pagination(string: str) -> bool:
    pattern = r"^[f]?to\s\d+$"
    match = re.match(pattern=pattern, string=string)
    if not match:
        return False
    return True
