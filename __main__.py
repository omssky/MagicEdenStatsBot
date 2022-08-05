import asyncio
import logging
import sys

from loader import bot, dp, db
import handlers

async def main() -> None:
    logging.basicConfig(level=logging.INFO, filename='data/logs.log', format="%(asctime)s | %(levelname)-5s | [%(module)s.%(funcName)s] > %(message)s")
    
    router = handlers.setup_routers()
    dp.include_router(router)

    await db.create_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    