import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import keyboards as kb
from rssfeeder import parse_names, fetch_news

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('здарова зайбал',
                         reply_markup=kb.mainmenu)


@user.message(F.text.lower() == 'читать новости')
async def news_menu(message: Message):
    await message.answer('Выберите издание',
                         reply_markup=kb.newsmenu)


@user.callback_query(F.data.startswith('news_'))
async def news_titles(callback: CallbackQuery):
    broadcaster = callback.data.split('_')[1]
    news_list = parse_names()
    builder = InlineKeyboardBuilder()
    for index, news in enumerate(news_list):
        builder.button(
            text=news,
            callback_data=f'fetch_{broadcaster}_{index}'
        )
    builder.adjust(1)
    await callback.message.answer(
        text='что хотите почитать?',
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@user.callback_query(F.data.startswith('fetch_'))
async def send_news(callback: CallbackQuery):
    broadcaster = callback.data.split('_')[1]
    number = int(callback.data.split('_')[2])
    news_text = fetch_news(broadcaster, number)
    await callback.message.answer(news_text)
    await callback.answer()