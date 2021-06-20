import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp, db
from states import Pass
from middlewares import _, __


@dp.message_handler(Text(__("Паспорт старого зразка")))
async def set_state_id(message: types.Message):
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    await message.answer(_("Сейчас вам предстоит передать нам ваши документы для оформления чипкарты\n"
                           "Отправьте пожалуйста первую страницу пасспорта"), reply_markup=ReplyKeyboardRemove())
    await Pass.doc1.set()


@dp.message_handler(state=Pass.doc1, content_types=types.ContentTypes.PHOTO)
async def get_passport_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Первая страница паспорта")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Отправьте пожалуйста вторую страницу паспорта")

        await Pass.doc2.set()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")


@dp.message_handler(state=Pass.doc2, content_types=types.ContentTypes.PHOTO)
async def get_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Вторая страница паспорта")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Отправьте пожалуйста страницу с пропиской")

        await Pass.doc3.set()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")


@dp.message_handler(state=Pass.doc3, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Страница с пропиской")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Отправьте пожалуйста лицевую сторону ваших прав"))

        await Pass.doc4.set()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")


@dp.message_handler(state=Pass.doc4, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Права, лицевая сторона")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Отправьте пожалуйста, заднюю сторону ваших прав"))

        await Pass.doc5.set()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")


@dp.message_handler(state=Pass.doc5, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Права, задняя сторона")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Отправьте пожалуйста ваш идентификационный код"))

        await Pass.doc6.set()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")


@dp.message_handler(state=Pass.doc6, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Идентификационный код")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Теперь отправьте следуюущий документ")

        await Pass.doc7.set()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")


@dp.message_handler(state=Pass.doc7, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Фотография для печати в фотоателье")
            except Exception as err:
                logging.exception(err)
        await message.answer(text="Спасибо ваши документы в обработке!")

        await state.reset_state()
    else:
        await message.answer(text="Ви відправити не фото, будь ласка, надішліть фотографію вашого документа")
