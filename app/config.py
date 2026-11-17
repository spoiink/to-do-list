import os

from dotenv import load_dotenv

load_dotenv()   # читает файл .env и кладёт значения в переменные окружения

DATABASE_URL = os.environ["DATABASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]
