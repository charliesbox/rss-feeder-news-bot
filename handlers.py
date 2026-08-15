import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
import keyboards as kb
from rssfeeder import *

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'привет! это тестовая версия моего бота-новостника\n'
                         'если вы из приемной комиссии МАИ, можете написать мне! @sbeu_bulka\n'
                         'чтобы начать, используй кнопку "Читать новости"',
                         reply_markup=kb.mainmenu)


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


@user.callback_query(F.data.startswith('agency_'))
async def departments_kb(callback: CallbackQuery):
    agency = callback.data.split('_')[1]
    deps = parse_departments(agency)
    builder = InlineKeyboardBuilder()
    for index, dep in enumerate(deps):
        builder.button(text=dep, callback_data=f'titles_{agency}_{index}_5')
    builder.adjust(2)
    try:
        await callback.message.edit_text(
            text = 'выберите раздел',
            reply_markup=builder.as_markup()
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


@user.callback_query(F.data.startswith('titles_'))
async def titles_kb(callback: CallbackQuery):
    agency = callback.data.split('_')[1]
    number = int(callback.data.split('_')[2])
    page_index = int(callback.data.split('_')[3])
    titles = parse_titles(agency, number)
    builder = InlineKeyboardBuilder()
    for index, title in enumerate(titles[page_index-5:page_index]):
        builder.button(text=title, callback_data=f'fetch_{agency}_{number}_{index}')
    if page_index < len(titles):
        builder.button(text='следующая страница', callback_data=f'titles_{agency}_{number}_{page_index + 5}')
    if page_index - 5 > 0:
        builder.button(text='предыдущая страница', callback_data=f'titles_{agency}_{number}_{page_index - 5}')
    builder.adjust(1)
    try:
        await callback.message.edit_text(
            text='что хотите почитать?',
            reply_markup=builder.as_markup()
    )
    except TelegramBadRequest:
        pass
    await callback.answer()

@user.callback_query(F.data.startswith('fetch_'))
async def get_news(callback: CallbackQuery):
    agency = callback.data.split('_')[1]
    number = callback.data.split('_')[2]
    index = int(callback.data.split('_')[3])
    newstext = fetch_news(agency, number, index)
    try:
        await callback.message.edit_text(
            text=newstext
        )
    except TelegramBadRequest:
        pass
    await callback.answer()