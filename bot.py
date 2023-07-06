import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from database.database_read import data_read, users_db
from handlers import other_handlers, user_handlers
from aiogram.fsm.storage.redis import RedisStorage, Redis
logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO,
                format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    
    logger.info('Starting bot')

    config: Config = load_config('.env')

    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')

    redis: Redis = Redis(host='localhost')
    storage: RedisStorage = RedisStorage(redis=redis)

    data_read('database/base.txt')
    dp: Dispatcher = Dispatcher(storage=storage)
    print(users_db)
    dp.include_router(user_handlers.main_router)
    dp.include_router(other_handlers.other_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


