# Example: https://docs.aiogram.dev/en/dev-3.x/dispatcher/middlewares.html

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        print("Before handler")
        result = await handler(event, data)
        print("After handler")
        return result
