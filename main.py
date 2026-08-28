import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from handlers import user
from dataparser import prepare_data

load_dotenv()


async def update_database():
    while True:
        await asyncio.to_thread(prepare_data())
        await asyncio.sleep(30 * 60)


async def main():
    PROXY_URL = os.getenv('PROXY_URL')
    if PROXY_URL:
        session = AiohttpSession(proxy=PROXY_URL)
    else:
        session = AiohttpSession()
    bot = Bot(token=os.getenv('BOT_TOKEN'), session=session)
    dp = Dispatcher()
    dp.include_router(user)
    asyncio.create_task(update_database())
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass