from aiogram import Bot, Dispatcher
from utils.database import DataBase
from config import TOKEN

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()
db = DataBase("data/database.db")
