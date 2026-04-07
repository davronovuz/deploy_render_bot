import asyncio
import logging
from loader import dp,bot
from handlers import setup_handlers
from middlewares.throttling import ThrottlingMiddleware

async def main()->None:
    # Barcha routerlarni ulash
    main_router=setup_handlers()
    dp.include_router(main_router)

    # antispam middleware
    dp.message.middleware(ThrottlingMiddleware(slow_mode_delay=3))

    await dp.start_polling(bot)
    logging.info("Bot ishga tushdi....")


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
