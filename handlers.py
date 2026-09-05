import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
import keyboards as kb
from rssfeeder import *
from config import NEWS_PER_PAGE

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'привет! это тестовая версия моего бота-новостника\n'
                         'чтобы начать, используй кнопку "Читать новости"',
                         reply_markup=kb.mainmenu)


# LATEST NEWS
@user.message(F.text.lower() == 'последние новости')
async def latest_news(message: Message):
    feed = parse_latest(0)
    answer_text_pieces = []

    builder = InlineKeyboardBuilder()
    for index, item in enumerate(feed[:10]):
        answer_text_pieces.append(
            f'{index + 1}. {item[3].upper()}, {item[4]}\n\n'
            f'{item[1]}\n'
            f'{item[2]}\n\n\n'
        )
        builder.button(text=str(index + 1), callback_data=f'fetch_{item[3]}_{item[0]}')
    if len(feed) > 10:
        builder.button(text='следующая страница', callback_data='latest_2')
    answer_text = ''.join(answer_text_pieces)
    builder.adjust(5)

    await message.answer(
        text=answer_text,
        reply_markup=builder.as_markup()
    )


# LATEST NEWS but with callbacks
@user.callback_query(F.data.startswith('latest_'))
async def latest_news_with_pages(callback: CallbackQuery):
    page = int(callback.data.split('_')[1])
    offset = (page - 1) * 10

    feed = parse_latest(offset)
    answer_text_pieces = []

    builder = InlineKeyboardBuilder()
    for index, item in enumerate(feed[:10]):
        answer_text_pieces.append(
            f'{index + 1}. {item[3].upper()}, {item[4]}\n\n'
            f'{item[1]}\n'
            f'{item[2]}\n\n\n'
        )
        builder.button(text=str(index + 1), callback_data=f'fetch_{item[0]}')
    answer_text = "".join(answer_text_pieces)
    builder.adjust(5)

    page_switchers = []
    if page > 1:
        page_switchers.append(InlineKeyboardButton(text='предыдущая страница', callback_data=f'latest_{page - 1}'))
    if len(feed) > 10:
        page_switchers.append(InlineKeyboardButton(text='следующая страница', callback_data=f'latest_{page + 1}'))
    builder.row(*page_switchers)

    try:
        await callback.message.edit_text(
            text=answer_text,
            reply_markup=builder.as_markup()
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


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
        builder.button(text=title[1], callback_data=f'fetch_{title[0]}')
    builder.adjust(1)

    page_switchers = []
    if page_offset > 0:
        page_switchers.append(InlineKeyboardButton(text='предыдущая страница',
                       callback_data=f'titles_{agency}_{dep_index}_{current_page - 1}'))
    if NEWS_PER_PAGE < len(titles):
        page_switchers.append(InlineKeyboardButton(text='следующая страница',
                    callback_data=f'titles_{agency}_{dep_index}_{current_page + 1}'))
    builder.row(*page_switchers)

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
    news_id = int(callback.data.split('_')[1])

    newstext = fetch_news(news_id)

    try:
        await callback.message.edit_text(
            text=newstext
        )
    except TelegramBadRequest:
        pass

    await callback.answer()