from typing import Optional

from aiogram.exceptions import TelegramAPIError
from loguru import logger

from loader import dp


@dp.errors()
async def errors_handler(update, exception) -> Optional[bool]:
    #  MUST BE THE  LAST CONDITION
    if isinstance(exception, TelegramAPIError):
        logger.error(f"TelegramAPIError: {exception} \nUpdate: {update}")
        return True

    # At least you have tried.
    logger.error(f"Update: {update} \n{exception}")
