from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from bot_core.handlers import make_list
from bot_core.loader import dp, bot
from bot_core.utils import check_pagination
from database.utils import user_service
from settings import SearchParameters


@dp.callback_query_handler(
    lambda callback: check_pagination(string=callback.data)
)
async def pagination(callback: CallbackQuery) -> None:
    page = int(callback.data.split(" ")[1])
    if callback.data.startswith("f"):
        return await make_list(
            message=callback.message,
            page=page,
            previous_message=callback.message,
            favorite=True,
        )
    return await make_list(
        message=callback.message, page=page, previous_message=callback.message
    )


@dp.callback_query_handler(lambda callback: callback.data == "city")
async def change_city(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(state=SearchParameters.city)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Киев", "Одесса", "Херсон")
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Выберите город",
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda callback: callback.data == "gender")
async def change_gender(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(state=SearchParameters.gender)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Для мужчин", "Для женщин", "Для подростков", "Универсальные")
    await state.set_state(SearchParameters.gender)

    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Выберите тип велосипеда",
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda callback: callback.data == "price")
async def change_price_range(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(SearchParameters.price_diapazon)

    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Введите диапазон цен(Пример: 0-50000):",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.callback_query_handler(lambda callback: callback.data == "stan")
async def change_state(callback: CallbackQuery, state: FSMContext) -> None:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Б/У", "Новые", "Все")
    await state.set_state(SearchParameters.stan)
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Выберите состояние",
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda callback: callback.data == "add_to_favorite")
async def add_to_favorite(callback: CallbackQuery) -> None:
    message_data = callback.message.text.split("\n")
    result = user_service.add_to_favorite(
        username=callback.from_user.username,
        name=message_data[0],
        price=message_data[1],
        date=message_data[2],
        link=message_data[3],
    )
    if result is False:
        return await callback.answer(text="Уже в избранном")
    return await callback.answer(text="Добавлено")


@dp.callback_query_handler(lambda callback: callback.data == "favorite")
async def favorite_list(callback: CallbackQuery) -> None:
    await make_list(message=callback.message, favorite=True)
