import asyncio
import json

import aiohttp
from aiogram.types import Message
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from settings import Config as c


def set_search_params(user_params: dict) -> dict:
    search_params = {
        "currency": "UAH",
        "search[order]": "created_at:desc",
        "search[filter_float_price:from]": user_params["price_from"],
        "search[filter_float_price:to]": user_params["price_to"],
        "search[filter_enum_gender]": user_params["gender"],
    }

    if user_params["stan"] != "Oba":
        search_params["search[filter_enum_state]"] = user_params["stan"]

    return search_params


async def get_bicycle_data(
    session: ClientSession, page: int, message: Message, user_params: dict
):
    search_params = set_search_params(user_params=user_params)

    if page > 1:
        search_params["page"] = page

    async with session.get(
        url=c.BICYCLE_URL + f"{user_params['city']}", params=search_params
    ) as response:
        if response.status == 404:
            return await message.answer(text="404")
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "html.parser")
        bicycles = soup.select(".css-1sw7q4x")

        data = {}
        for bicycle in bicycles[:-1]:
            bicycle_link = c.DOMAIN + bicycle.select_one("a")["href"]
            bicycle_name = bicycle.select_one("h6").text
            bicycle_price = bicycle.select_one(
                "p[data-testid='ad-price']"
            ).text
            date = bicycle.select_one("p[data-testid='location-date']").text

            data[bicycle_link] = {
                "bicycle": bicycle_name,
                "price": bicycle_price,
                "date": date,
                "link": bicycle_link,
            }
        await c.storage.set(
            name=message.from_user.username, value=json.dumps(data)
        )


async def gather_data(message: Message, user_params: dict) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []

        for page in range(1, c.PAGES_COUNT + 1):
            task = asyncio.create_task(
                get_bicycle_data(session, page, message, user_params)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
