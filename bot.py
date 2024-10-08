import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from loader import bot, dp
from tgbot.config import Settings, config
from tgbot.handlers.scheduled_messages import scheduled_notification
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.settings import ConfigMiddleware
from tgbot.middlewares.storage import StorageMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.misc.database import Database
from tgbot.misc.storage import Storage
from tgbot.models.models import close_db, init
from tgbot.services.admins_notify import on_startup_notify
from tgbot.services.setting_commands import set_default_commands


def register_all_handlers() -> None:
    from tgbot import handlers  # noqa: F401

    logging.info("Handlers registered.")


async def register_all_commands(bot: Bot) -> None:
    await set_default_commands(bot)
    logging.info("Commands registered.")


def register_global_middlewares(dp: Dispatcher, config: Settings):
    middlewares = [
        ConfigMiddleware(config),
        ThrottlingMiddleware(),
        DatabaseMiddleware(Database()),
        StorageMiddleware(
            Storage(
                config.access_id.get_secret_value(),
                config.access_key.get_secret_value(),
                config.bucket_name,
                config.region_name,
            )
        ),
    ]

    for middleware in middlewares:
        dp.message.outer_middleware(middleware)
        dp.callback_query.outer_middleware(middleware)

    # dp.callback_query.middleware(
    #     CallbackAnswerMiddleware(pre=True, text="Ready!", show_alert=True)
    # )
    logging.info("Middlewares registered.")


async def init_database():
    await init()
    logging.info("Database was inited")


async def start_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        scheduled_notification,
        trigger="date",
        run_date=datetime.now() + timedelta(seconds=10),
        kwargs={"bot": bot, "db": Database()},
    )
    logging.info("Scheduler was inited")


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    register_all_handlers()
    register_global_middlewares(dispatcher, config)
    await init_database()
    await register_all_commands(bot)
    await on_startup_notify(bot)
    await start_scheduler(bot)
    logging.info("Bot started.")


async def on_shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()
    logging.info("Storage closed.")
    await close_db()
    logging.info("Database was closed.")
    logging.info("Bot stopped.")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # And the run events dispatching
    await dp.start_polling(bot)
    # * For the webhook usage:
    # * https://docs.aiogram.dev/en/dev-3.x/dispatcher/webhook.html#examples


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="bot.log",
        format="%(asctime)s :: %(levelname)s :: %(module)s.%(funcName)s :: %(lineno)d :: %(message)s",  # noqa: E501
        filemode="w",
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
