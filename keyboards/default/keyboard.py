from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from middlewares import __

lang_button = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="UA"),
        KeyboardButton(text="RU"),
        KeyboardButton(text="EN")
    ]
], one_time_keyboard=True)

passport_choice = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text=__("Паспорт нового зразка")),
        KeyboardButton(text=__("Паспорт старого зразка"))
    ]
], one_time_keyboard=True)
