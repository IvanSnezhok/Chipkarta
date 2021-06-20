import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.keyboard import lang_button, passport_choice
from loader import dp, db
from middlewares import _, __


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)
    await message.answer(_(f"Вітаю, {message.from_user.full_name}!"))
    await message.answer(_("Оберіть зручну для вас мову!"), reply_markup=lang_button)



@dp.message_handler(Text(["UA", "RU", "EN"]))
async def tel_info(message: types.Message):
    await db.set_lang(message.text.lower(), message.from_user.id)
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    await message.answer(_("Тепер будь-ласка відправте свій номер телефона для зв`язку з вами"),
                         reply_markup= ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="📱",
                       request_contact=True)
    ]
], one_time_keyboard=True))


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def about_bot(message: types.Message):
    await db.update_phone_number(message.contact.phone_number, message.from_user.id)
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    await message.answer(_("Тут буде опис бота, на следуюущей кнопці можна перейти на відправку документів\n"
                           "Потрібно тільки вибрати який паспорт у тебе"), reply_markup=passport_choice)


