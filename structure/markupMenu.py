from aiogram import types

#Основное меню
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

menu_catalog = types.KeyboardButton('Каталог')
menu_profile = types.KeyboardButton('Профиль')
menu_cart = types.KeyboardButton('Корзина')
menu_favorites = types.KeyboardButton('Избранное')
menu_settings = types.KeyboardButton('Настройки')
menu_help = types.KeyboardButton('Помощь')

markup_menu.add(menu_catalog, menu_profile, menu_cart, menu_favorites, menu_settings, menu_help)