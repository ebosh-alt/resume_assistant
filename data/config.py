import datetime

from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(bot_token)
SQLALCHEMY_DATABASE_URL = env("SQLALCHEMY_DATABASE_URL")
TZ_INFO = int(env("TZ_INFO"))
offset = datetime.timedelta(hours=TZ_INFO)
YKASSA_API_KEY = env("YKASSA_API_KEY")
BASE_PATH_PDF = "./data/pdf/"
FORMAT_FILES = ["pdf", "docx", "txt"]
OPENAI_API_KEY = env("OPENAI_API_KEY")
ASSISTANT = env("ASSISTANT")
count_free_request = 3
allowed_file_len = 30000
