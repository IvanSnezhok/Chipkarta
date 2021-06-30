import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default.keyboard import return_button
from loader import dp, db
from states import PassId
from middlewares import _, __


@dp.message_handler(Text([__("Паспорт нового зразка")]))
async def set_state_id(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    if user[1]:
        await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
        msg = await message.answer(_("Зараз необхідно передати скани чи фото Ваших документів для оформлення чіпкарти\n"
                               "Надішліть, будь-ласка, лицьову сторону паспорту"), reply_markup=ReplyKeyboardRemove())
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc1.set()
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, text=f"Пользователь с именем: {user[0]} и телефоном: {user[1]}\n"
                                                      f"Готовиться отправить документы")
            except Exception as err:
                logging.exception(err)
    else:
        msg = await message.answer(_("У нас відсутня інформація про ваш номер телефону, будь ласка пройдіть регістрацю ще раз"
                               "Для цього увведіть /start"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc1, content_types=types.ContentTypes.PHOTO)
async def get_passport_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Лицевая сторона пасспорта")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Надішліть іншу сторону паспорту"))
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc2.set()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc2, content_types=types.ContentTypes.PHOTO)
async def get_id(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Задняя сторона паспорта")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Відправте фото витягу паспорту"))
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc3.set()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc3, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Витяг про прописку")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Надішліть будь ласка лицьову сторону ваших прав"))
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc4.set()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc4, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Права, лицевая сторона")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Надішліть будь ласка, іншу сторону прав"))
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc5.set()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc5, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Права, задняя сторона")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Відправте Ваш ідентифікаційний код"))
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc6.set()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc6, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Идентификационный код")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Тепер відправте будь ласка ваше фото для друку в анкету"))
        await db.message("BOT", 10001, msg.text, message.date)

        await PassId.doc7.set()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)


@dp.message_handler(state=PassId.doc7, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        for admin in ADMINS:
            try:
                await dp.bot.send_photo(admin, message.photo[-1].file_id, "Фотография для печати в фотоателье")
            except Exception as err:
                logging.exception(err)
        msg = await message.answer(text=_("Дякую, Ваші документи в обробці!"),
                                   reply_markup=return_button)
        await db.message("BOT", 10001, msg.text, message.date)

        await state.reset_state()
    else:
        msg = await message.answer(text=_("Ви відправили не фото, будь ласка, надішліть фотографію вашого документа"))
        await db.message("BOT", 10001, msg.text, message.date)
