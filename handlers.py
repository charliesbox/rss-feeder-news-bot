import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
import keyboards as kb
from rssfeeder import *
from config import NEWS_PER_PAGE

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'привет! это тестовая версия моего бота-новостника\n'
                         'если вы из приемной комиссии МАИ, можете написать мне! @sbeu_bulka\n'
                         'чтобы начать, используй кнопку "Читать новости"',
                         reply_markup=kb.mainmenu)


# CHOOSING NEWS AGENCY
@user.message(F.text.lower() == 'читать новости')
async def agencies_kb(message: Message):
    agencies = parse_agencies()

    builder = InlineKeyboardBuilder()
    for agency in agencies:
        builder.button(text=agency.upper(), callback_data=f'agency_{agency}')
    builder.adjust(1)

    await message.answer(
        text='выберите агентство',
        reply_markup=builder.as_markup()
    )


# CHOOSING DEPARTMENTS
@user.callback_query(F.data.startswith('agency_'))
async def departments_kb(callback: CallbackQuery):
    agency = callback.data.split('_')[1]

    deps = parse_departments(agency)

    builder = InlineKeyboardBuilder()
    for dep_index, dep in enumerate(deps):
        builder.button(text=dep, callback_data=f'titles_{agency}_{dep_index}_1')
    builder.adjust(2)

    try:
        await callback.message.edit_text(
            text = 'выберите раздел',
            reply_markup=builder.as_markup()
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


# CHOOSING A TITLE & PAGE SWITCHING
@user.callback_query(F.data.startswith('titles_'))
async def titles_kb(callback: CallbackQuery):
    agency = callback.data.split('_')[1]
    dep_index = int(callback.data.split('_')[2])
    current_page = int(callback.data.split('_')[3])
    page_offset = (current_page - 1) * NEWS_PER_PAGE

    titles = parse_titles(agency, dep_index, NEWS_PER_PAGE + 1, page_offset)

    builder = InlineKeyboardBuilder()
    for title in titles[:NEWS_PER_PAGE]:
        builder.button(text=title[1], callback_data=f'fetch_{agency}_{title[0]}')
    if NEWS_PER_PAGE < len(titles):
        builder.button(text='следующая страница',
                    callback_data=f'titles_{agency}_{dep_index}_{current_page + 1}')
    if page_offset > 0:
        builder.button(text='предыдущая страница',
                       callback_data=f'titles_{agency}_{dep_index}_{current_page - 1}')
    builder.adjust(1)

    try:
        await callback.message.edit_text(
            text='что хотите почитать?',
            reply_markup=builder.as_markup()
    )
    except TelegramBadRequest:
        pass

    await callback.answer()


# GETTING THE NEWS
@user.callback_query(F.data.startswith('fetch_'))
async def get_news(callback: CallbackQuery):
    agency = callback.data.split('_')[1]
    news_id = callback.data.split('_')[2]

    newstext = fetch_news(agency, news_id)

    try:
        await callback.message.edit_text(
            text=newstext
        )
    except TelegramBadRequest:
        pass

    await callback.answer()