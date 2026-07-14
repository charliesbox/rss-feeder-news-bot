from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

mainmenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Читать новости')]
    ],
    resize_keyboard=True,
    input_field_placeholder='это все равно тест'
)
