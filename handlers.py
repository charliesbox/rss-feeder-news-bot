import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
import keyboards as kb
from rssfeeder import parse_agencies, parse_departments, parse_titles, fetch_news

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
    for index, dep in enumerate(deps):
        builder.button(text=dep, callback_data=f'titles_{agency}_{index}_1')
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
    number = int(callback.data.split('_')[2])
    page_offset = int(callback.data.split('_')[3]) * 5    #this '* 5' can customize the amount of titles in one page

    titles = await parse_titles(agency, number)

    builder = InlineKeyboardBuilder()
    for index, title in enumerate(titles[page_offset-5:page_offset]):
        builder.button(text=title, callback_data=f'fetch_{agency}_{number}_{index}')
    if page_offset < len(titles):
        builder.button(text='следующая страница', callback_data=f'titles_{agency}_{number}_{(page_offset // 5) + 1}')    #if you're customizing the amount of news in one page,
    if page_offset - 5 > 0:                                                                                              #make sure to change the respective number here too
        builder.button(text='предыдущая страница', callback_data=f'titles_{agency}_{number}_{(page_offset // 5) - 1}')
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
    number = callback.data.split('_')[2]
    index = int(callback.data.split('_')[3])

    newstext = await fetch_news(agency, number, index)

    try:
        await callback.message.edit_text(
            text=newstext
        )
    except TelegramBadRequest:
        pass

    await callback.answer()