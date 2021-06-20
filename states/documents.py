from aiogram.dispatcher.filters.state import StatesGroup, State


class PassId(StatesGroup):
    doc1 = State()  # Пасспорт лицевая сторона
    doc2 = State()  # Пасспорт задняя сторона
    doc3 = State()  # Витяг пасорта
    doc4 = State()  # Права лицевая сторона
    doc5 = State()  # Права задняя сторона
    doc6 = State()  # Индефикационный код
    doc7 = State()  # Фото лица на светлом фоне


class Pass(StatesGroup):
    doc1 = State()  # Пасспорт 1 ст.
    doc2 = State()  # Пасспорт 2 ст.
    doc3 = State()  # Страница с пропиской
    doc4 = State()  # Права лицевая сторона
    doc5 = State()  # Права задняя сторона
    doc6 = State()  # Индефикационный код
    doc7 = State()  # Фото лица на светлом фоне
