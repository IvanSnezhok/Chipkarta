import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp, db
from states import PassId
from middlewares import _, __


@dp.message_handler(Text(__("Паспорт нового зразка")))
async def set_state_id(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    if user[1]:
        await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
        await message.answer(_("Зараз ви маєте передати нам ваші документи для оформлення чіпкарти\n"
                               "Надішліть будь ласка лицьову сторону паспорта"), reply_markup=ReplyKeyboardRemove())

        await PassId.doc1.set()
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, text=f"Пользователь с именем: {user[0]} и телефоном: {user[1]}\n"
                                                      f"Готовиться отправить документы")
            except Exception as err:
                logging.exception(err)
    else:
        await message.answer(_("У нас відсутня інформація про ваш номер телефону, будь ласка пройдіть регістрацю ще раз"
                               "Для цього увведіть /start"))


@dp.message_handler(state=PassId.doc1, content_types=types.ContentTypes.PHOTO)
async def get_passport_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Лицевая сторона пасспорта")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Будь ласка надішліть задню сторону паспорта"))

        await PassId.doc2.set()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))


@dp.message_handler(state=PassId.doc2, content_types=types.ContentTypes.PHOTO)
async def get_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Задняя сторона паспорта")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Теперь отправьте следуюущий документ"))

        await PassId.doc3.set()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))


@dp.message_handler(state=PassId.doc3, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Витяг про прописку")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Теперь отправьте следуюущий документ"))

        await PassId.doc4.set()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))


@dp.message_handler(state=PassId.doc4, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Права, лицевая сторона")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Теперь отправьте следуюущий документ"))

        await PassId.doc5.set()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))


@dp.message_handler(state=PassId.doc5, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Права, задняя сторона")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Теперь отправьте следуюущий документ"))

        await PassId.doc6.set()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))


@dp.message_handler(state=PassId.doc6, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Идентификационный код")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Теперь отправьте следуюущий документ"))

        await PassId.doc7.set()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))


@dp.message_handler(state=PassId.doc7, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Фотография для печати в фотоателье")
            except Exception as err:
                logging.exception(err)
        await message.answer(text=_("Спасибо ваши документы в обработке!"))

        await state.reset_state()
    else:
        await message.answer(text=_("Ви відправити не фото, будь ласка, надішліть фотографію вашого документа"))
