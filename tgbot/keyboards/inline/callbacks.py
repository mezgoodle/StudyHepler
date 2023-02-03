# Example: https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/callback_data.html


from typing import Optional

from aiogram.filters.callback_data import CallbackData


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]
