from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from forecaster import get_coords, send_request
from utils import parse_json, parse_to_display, display_all_history, parse_query_to_story
from db import get_queries, save_query, clear_queries, get_queries_count
from dotenv import load_dotenv
import json
import os

load_dotenv()

TOKEN = os.environ.get('telegram_token')
YANDEX_URL = 'https://api.weather.yandex.ru/graphql/query'
YANDEX_ACCESS_KEY = os.environ.get('access_key')

app = FastAPI()

class QueryData(BaseModel):
    user_id: int
    city: str
    weather: dict

@app.get('/weather/{city}')
async def get_weather(city: str):
    coords = get_coords(city)
    if coords is None:
        raise HTTPException(status_code=404, detail='Город не найден')
    
    data = await send_request(YANDEX_URL, YANDEX_ACCESS_KEY, coords)
    if data is None:
        raise HTTPException(status_code=503, detail='Ошибка API')
    
    weather = parse_json(data)
    if weather is None:
        raise HTTPException(status_code=500, detail='Ошибка парсинга')
    
    return {
        'city': city,
        'weather': parse_to_display(weather, city),
        'row': data
    }

@app.post('/history')
def save_query_to_history(query_data: QueryData):
    save_query(query_data.user_id, query_data.city, query_data.weather)
    return {'status': 'ok'}

@app.get('/history/{user_id}')
def get_history(user_id: int):  
    queries = get_queries(user_id)
    count = get_queries_count(user_id)
    queries_to_display_count = len(queries)
    answers_data = []
    for city, json_data, query_date in queries:
        dict_data = json.loads(json_data)
        weather_data = parse_json(dict_data)
        answer = parse_query_to_story(weather_data, city, query_date)
        answers_data.append(answer)

    return {
        'total': count,
        'total_to_display': queries_to_display_count,
        'history': display_all_history(answers_data, queries_to_display_count, count)
    }

@app.delete('/history/{user_id}')
def delete_history(user_id: int):
    clear_queries(user_id)
    return {'status' : 'ok'}