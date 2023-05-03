import json

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from settings import Config as c
from bot_core.loader import dp, bot
from bot_core.utils import (
    price_from_to,
    validate_price_range,
    make_keyboard,
    make_message_text,
    settings_keyboard,
)
from database.utils import user_service
from parser import gather_data
from settings import SearchParameters


@dp.message_handler(Command("start"))
async def send_hello(message: Message, state: FSMContext) -> None:
    user = user_service.get_user_by_username(
        username=message.from_user.username
    )
    if user:
        await message.reply(
            text="У вас уже есть аккаунт", reply_markup=ReplyKeyboardRemove()
        )
        return await settings_message(message=message)

    await state.set_state(SearchParameters.price_diapazon)
    await message.reply(
        text="Введите диапазон цен(Пример: 0-50000):",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(
    lambda message: not validate_price_range(_range=message.text),
    state=SearchParameters.price_diapazon,
)
async def process_price_invalid(message: Message) -> Message:
    return await message.reply(
        text="Invalid price", reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(
    lambda message: validate_price_range(_range=message.text),
    state=SearchParameters.price_diapazon,
)
async def process_price_from(
    message: Message, state: FSMContext
) -> None | Message:
    await state.update_data(price_diapazon=message.text)
    price_from, price_to = price_from_to(range_price=message.text)
    await state.update_data(price_from=price_from)
    await state.update_data(price_to=price_to)

    user = user_service.get_user_by_username(
        username=message.from_user.username
    )
    if user:
        user_service.update_user_settings(
            user=user,
            price_from=price_from,
            price_to=price_to,
        )
        await state.finish()
        await message.answer(
            text="Диапазон цен изменен", reply_markup=ReplyKeyboardRemove()
        )
        return await settings_message(message=message)
    await state.set_state(state=SearchParameters.city)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Киев", "Одесса", "Херсон")
    await message.reply(text="Выберите город", reply_markup=markup)


@dp.message_handler(
    lambda message: message.text not in c.CITIES, state=SearchParameters.city
)
async def invalid_city(message: Message) -> Message:
    return await message.reply(text="Город не в базе")


@dp.message_handler(
    lambda message: message.text in c.CITIES, state=SearchParameters.city
)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=c.CITIES[message.text])
    user = user_service.get_user_by_username(
        username=message.from_user.username
    )
    if user:
        user_service.update_user_settings(
            user=user, city=c.CITIES[message.text]
        )
        await state.finish()
        await message.answer(
            "Город изменен", reply_markup=ReplyKeyboardRemove()
        )
        return await settings_message(message=message)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Б/У", "Новые", "Все")
    await state.set_state(SearchParameters.stan)
    await message.reply(text="Выберите состояние", reply_markup=markup)


@dp.message_handler(
    lambda message: message.text not in c.STAN,
    state=SearchParameters.stan,
)
async def invalid_stan(message: Message) -> Message:
    return await message.reply(text="Нет такого состояния")


@dp.message_handler(
    lambda message: message.text in c.STAN,
    state=SearchParameters.stan,
)
async def process_stan(message: Message, state: FSMContext) -> None:
    await state.update_data(stan=c.STAN[message.text])
    user = user_service.get_user_by_username(
        username=message.from_user.username
    )
    if user:
        user_service.update_user_settings(
            user=user, state=c.STAN[message.text]
        )
        await state.finish()
        await message.answer(
            text="Состояние изменено", reply_markup=ReplyKeyboardRemove()
        )
        return await settings_message(message=message)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Для мужчин", "Для женщин", "Для подростков", "Универсальные")

    await state.set_state(SearchParameters.gender)

    await message.reply(text="Выберите тип велосипеда", reply_markup=markup)


@dp.message_handler(
    lambda message: message.text not in c.GENDER,
    state=SearchParameters.gender,
)
async def invalid_gender(message: Message) -> Message:
    return await message.reply(text="Нет такого типа")


@dp.message_handler(
    lambda message: message.text in c.GENDER,
    state=SearchParameters.gender,
)
async def process_gender(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=c.GENDER[message.text])
    user = user_service.get_user_by_username(
        username=message.from_user.username
    )
    if user:
        user_service.update_user_settings(
            user=user, gender=c.GENDER[message.text]
        )
        await state.finish()
        await message.answer(
            text="Тип был изменен", reply_markup=ReplyKeyboardRemove()
        )
        return await settings_message(message=message)
    user_data = await state.get_data()
    user_service.create_user(
        username=message.from_user.username,
        price_from=user_data["price_from"],
        price_to=user_data["price_to"],
        state=user_data["stan"],
        gender=user_data["gender"],
        city=user_data["city"],
    )
    await state.finish()
    await settings_message(message=message)


@dp.message_handler(Command("settings"))
async def settings_message(message: Message) -> None | Message:
    user = await bot.get_chat(chat_id=message.chat.id)
    user = user_service.get_user_by_username(username=user.username)
    if user is None:
        return await message.reply(
            text="У вас нет профиля, /start для регистрации"
        )
    message_text = f"Город: {user.search_params.city}\nТип велосипеда: {user.search_params.gender}\nСостояние: {user.search_params.state}\nОт(грн.):{user.search_params.price_from}\nДо(грн.):{user.search_params.price_to}"
    keyboard = settings_keyboard()
    await message.answer(text=message_text, reply_markup=keyboard)


@dp.message_handler(Command("parse"))
async def start_parsing(message: Message) -> None:
    user = user_service.get_user_by_username(
        username=message.from_user.username
    )
    user_data = {
        "price_from": user.search_params.price_from,
        "price_to": user.search_params.price_to,
        "gender": user.search_params.gender,
        "stan": user.search_params.state,
        "city": user.search_params.city,
    }
    await gather_data(message=message, user_params=user_data)

    await make_list(message=message)


async def make_list(
    message: Message, page=1, previous_message=None, favorite: bool = False
) -> None | Message:
    user = await bot.get_chat(chat_id=message.chat.id)

    if favorite:
        user = user_service.get_user_by_username(username=user.username)
        favorites = user.favorites
        pages_count = len(favorites)
        keyboard = make_keyboard(
            page=page, pages_count=pages_count, favorite=True
        )
        if pages_count == 0:
            text_message = "Ваше избранное пустое"
            await message.answer(
                text=text_message, reply_markup=ReplyKeyboardRemove()
            )
            return await settings_message(message=message)
        text_message = make_message_text(page=page, favorites=favorites)
        await message.answer(text=text_message, reply_markup=keyboard)
    else:
        result = await c.storage.get(name=user.username)
        result = json.loads(result.decode("utf-8"))
        pages_count = len(result)
        keyboard = make_keyboard(page=page, pages_count=pages_count)
        text_message = make_message_text(page=page, result=result)
        await message.answer(text_message, reply_markup=keyboard)
    try:
        await bot.delete_message(
            chat_id=message.chat.id, message_id=previous_message.message_id
        )
    except AttributeError:
        pass
