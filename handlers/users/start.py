from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from keyboards.default.keyboard import lang_button, passport_choice
from loader import dp
from middlewares import _, __


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(_(f"Вітаю, {message.from_user.full_name}!"))
    await message.answer(_("Оберіть зручну для вас мову!"), reply_markup=lang_button)


@dp.message_handler(Text("UA","RU","EN"))
async def about_bot(message: types.Message):
    await message.answer(_("Тут будет описание бота, на следуюущей кнопке можно перейти на отправку документов\n"
                           "Нужно только выбрать какой паспорт у тебя"), reply_markup=passport_choice)


