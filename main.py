import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from handlers import user

load_dotenv()

async def main():
    PROXY_URL = os.getenv('PROXY_URL')
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=os.getenv('BOT_TOKEN'), session=session)
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass