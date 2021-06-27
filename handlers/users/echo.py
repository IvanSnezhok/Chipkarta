from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.keyboard import return_button
from loader import dp, db
from middlewares import _, __


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    msg = await message.answer(_("Для взаємодії з ботом нажміть кнопку"), reply_markup=return_button)
    await db.message("BOT", 10001, msg, message.date.time())


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    msg = await message.answer(_("Будь-ласка, користуйтесь згідно інструкції1"))
    await db.message("BOT", 10001, msg, message.date.time())