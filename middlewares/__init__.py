from aiogram import Dispatcher

from loader import dp
from .lang_middleware import setup_middleware, ACLMiddleware
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    i18n = setup_middleware(dp)
    _ = i18n.gettext
    __ = i18n.lazy_gettext
