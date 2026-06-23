from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv
import asyncio
import httpx
import os

load_dotenv()

TOKEN = os.environ.get('telegram_token')
YANDEX_URL = 'https://api.weather.yandex.ru/graphql/query'
YANDEX_ACCESS_KEY = os.environ.get('access_key')
FASTAPI_URL = 'http://localhost:8000'

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer('Привет! Я погодный бот.')

@dp.message(Command('weather'))
async def send_weather(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    city = command.args
    if city is None:
        city = 'Тюмень'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{FASTAPI_URL}/weather/{city}')
        data = response.json()
        answer = data['weather']

    try:
        data = {
            "user_id": user_id,
            "city": city,
            "weather": data['row']
        }   
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{FASTAPI_URL}/history', json=data)
    except:
        await message.answer('При сохранении запроса в историю произошла ошибка. На данные прогноза это не повлияет.')

    await message.answer(answer)

@dp.message(Command('help'))
async def help_command(message: types.Message, command: CommandObject):
    answer = 'На данный момент доступны команды:\n' \
            '/weather [город] — бот покажет погоду по названию города / базовое значение — Тюмень;\n' \
            '/history — бот покажет последние 10 запросов;\n' \
            '/history clear — бот очистит историю запросов'
    await message.answer(answer)

@dp.message(Command('history'))
async def history_command(message: types.Message, command: CommandObject):
    arg = command.args
    user_id = message.from_user.id
    if arg is None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f'{FASTAPI_URL}/history/{user_id}')
                data = response.json()

            if data['total'] == 0:
                await message.answer('История запросов пуста.')
                return
            answer = data['history']
            await message.answer(answer)
        except Exception:
            await message.answer('При обращении к базе данных произошла непредвиденная ошибка. Попробуйте позже.')
    elif arg == 'clear':
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f'{FASTAPI_URL}/history/{user_id}')
            await message.answer('История запросов успешно очищена.')
        except:
            await message.answer('При очистке истории произошла ошибка. Попробуйте позже')
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())