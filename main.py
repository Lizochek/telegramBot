from cgitb import handler
from email import message
from gettext import Catalog
import sqlite3
import config
import messages
from structure import markupMenu, menuCatalog, menuProfile
from database.img import *
from database.furniture import furniture
from page import page

from config import API_TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

furniture_callback = CallbackData("Furniture", "page")


#БД
#conn = sqlite3.connect('database/users.db', check_same_thread=False)
#cursor = conn.cursor()
#def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
#	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
#	conn.commit()
#db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)


#Старт
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    
    await message.answer("🏠")
    await message.answer( us_name+messages.HELLO_MESSAGE, reply_markup=markupMenu.markup_menu)
    await message.answer(message.chat.id, messages.INFO_MESSAGE)


#Меню
@dp.message_handler(content_types='text')
async def inline_catalog(message: types.Message):
    #Каталог
    if message.text == 'Каталог':
        catalog = furniture[0]
        caption = f"Вы выбрали <b>{catalog.get('display_name')}</b>"
        keyboard = get_furniture_keyboard()  # Page: 0

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=catalog.get("image_url"),
            caption=caption,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    #Профиль
    elif message.text == 'Профиль':
        await bot.send_message(message.chat.id, 'Профиль')
    #Корзина
    elif message.text == 'Корзина':
        bot.send_message(message.chat.id, 'Корзина')
    #Избранное
    elif message.text == 'Избранное':
        bot.send_message(message.chat.id, 'Избранное')
    #Настройки
    elif message.text == 'Настройки':
        bot.send_message(message.chat.id, 'Настройки')
    #Помощь
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id, 'Помощь')
    

#Галерея
def get_furniture_keyboard(page: int = 0) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    has_next_page = len(furniture) > page + 1
    
    if page != 0 & has_next_page:
        keyboard.add(
            types.InlineKeyboardButton(
                text="< Назад",
                callback_data=furniture_callback.new(page=page - 2)
            ),
            types.InlineKeyboardButton(
                text="Вперёд >",
                callback_data=furniture_callback.new(page=page + 1)
            )
        )
    elif page != 0:
        keyboard.add(
            types.InlineKeyboardButton(
                text="< Назад",
                callback_data=furniture_callback.new(page=page - 1)
            )
        )
    elif has_next_page:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Вперёд >",
                callback_data=furniture_callback.new(page=page + 1)
            )
        )

    
    keyboard.add(
        types.InlineKeyboardButton(
            text=f"• {page + 1} •",
            callback_data="dont_click_me"
        )
    )

    return keyboard




@dp.callback_query_handler(furniture_callback.filter())
async def furniture_page_handler(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))

    catalog = furniture[page]
    caption = f"Вы выбрали <b>{catalog.get('display_name')}</b>"
    keyboard = get_furniture_keyboard(page)

    photo = types.InputMedia(type="photo", media=catalog.get("image_url"), caption=caption)

    await bot.edit_media(photo, keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)