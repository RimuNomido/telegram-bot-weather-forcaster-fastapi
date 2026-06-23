import sqlite3
import json

db_name = 'queries.db'

def init_db():
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            user_id INTEGER,
            city TEXT NOT NULL,
            weather_data JSON,
            query_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        connection.commit()

init_db()

def save_query(user_id, city, weather_data):
    data = json.dumps(weather_data, ensure_ascii=False)
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO queries (user_id, city, weather_data) VALUES (?, ?, ?)', (user_id, city, data))


def get_queries(user_id):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT city, weather_data, datetime(query_date, "localtime") FROM queries WHERE user_id = ? ORDER BY query_date DESC LIMIT 10', (user_id,))
        rows = cursor.fetchall()
        return rows
    
def get_queries_count(user_id):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM queries WHERE user_id = ?', (user_id,))
        total = cursor.fetchone()[0]
        return total

def clear_queries(user_id):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM queries WHERE user_id = ?', (user_id,))