from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import SupportCallbackFactory


async def support_keyboard(
    messages: str, teacher_id: int | None = None, user_id: int | None = None
) -> InlineKeyboardMarkup:
    if user_id:
        contact_id = user_id
        as_user = False
        text = "Answer to student"
    else:
        contact_id = teacher_id
        as_user = True
        if messages == "one":
            text = "Write your message"
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=SupportCallbackFactory(
                messages=messages, user_id=contact_id, as_user=as_user
            ).pack(),
        )
    )
    return keyboard.as_markup()
