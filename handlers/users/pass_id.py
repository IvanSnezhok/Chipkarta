import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp
from states import Doc


@dp.message_handler(state=Doc.doc1, content_types=types.ContentTypes.PHOTO)
async def get_passport_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Первый документ")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Теперь отправьте следуюущий документ")

        await Doc.doc2.set()
    else:
        await message.answer(text="Вы отправили не фото, пожалуйста, отправьте фотографию вашего документа")


@dp.message_handler(state=Doc.doc2, content_types=types.ContentTypes.PHOTO)
async def get_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Второй документ")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Теперь отправьте следуюущий документ")

        await Doc.doc3.set()
    else:
        await message.answer(text="Вы отправили не фото, пожалуйста, отправьте фотографию вашего документа")


@dp.message_handler(state=Doc.doc3, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Третий документ")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Спасибо ваши документы в обработке!")

        await state.reset_state()
    else:
        await message.answer(text="Вы отправили не фото, пожалуйста, отправьте фотографию вашего документа")