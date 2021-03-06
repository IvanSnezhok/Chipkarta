import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    logging.info("Создаем подключение к локальной ДБ")
    await db.create()
    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()
    logging.info("Создаем таблицу сообщений")
    await db.create_table_msg()
    logging.info("Готово.")
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
