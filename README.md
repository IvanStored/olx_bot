# ТГ бот для парсинга цен с ОЛХ

Бот позволяет парсить цены на велосипеды в трех городах (планируется расширить):
- Киев
- Херсон
- Одесса

Есть возможность выбора следующих параметров:
- тип велосипеда(мужской, женский, для подростков, универсальный)
- состояние(б\у, новые, все)
- ценовой диапазон

###  Так же есть возможность добавить обьявление в "Избранное"


# Проверить (Убедитесь, что у вас есть юзернейм в телеграмме!!!!):
https://t.me/olx_bicyclebot
# Installation:

```sh
git clone https://github.com/IvanStored/olx_bot.git
cd olx_bot
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
Create .env file follow by .env.sample
docker compose up --build
```
