from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

#Разворот
#catalog_menu2 = types.InlineKeyboardMarkup(row_width=3)
#catalog_popular = types.InlineKeyboardButton(text="Популярное", callback_data="Популярное")
#catalog_sofa = types.InlineKeyboardButton(text="Диваны", callback_data="Диваны")
#catalog_closet = types.InlineKeyboardButton(text='Шкафы', callback_data="Шкафы")
#catalog_menu2.add(catalog_sofa, catalog_closet, catalog_popular)


catalog_menu = types.InlineKeyboardMarkup(row_width=2)
catalog_back = types.InlineKeyboardButton(text='◀️', callback_data="Назад")
catalog_forword = types.InlineKeyboardButton(text='▶️', callback_data="Вперед")
catalog_menu.add(catalog_back, catalog_forword)

