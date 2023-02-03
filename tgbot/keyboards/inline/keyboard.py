from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import NumbersCallbackFactory


async def inline_keyboard(bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="GitHub", url="https://github.com"))
    builder.row(
        InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=telegram")
    )

    # user_id = 1234567890
    # chat_info = await bot.get_chat(user_id)
    # if not chat_info.has_private_forwards:
    #     builder.row(InlineKeyboardButton(text="User", url=f"tg://user?id={user_id}"))

    return builder.as_markup()


def random_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Press", callback_data="random_value"))
    return builder.as_markup()


def big_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="-2", callback_data=NumbersCallbackFactory(action="change", value=-2)
    )
    builder.button(
        text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1)
    )
    builder.button(
        text="+1", callback_data=NumbersCallbackFactory(action="change", value=1)
    )
    builder.button(
        text="+2", callback_data=NumbersCallbackFactory(action="change", value=2)
    )
    builder.button(
        text="Confirm", callback_data=NumbersCallbackFactory(action="finish")
    )
    builder.adjust(4)
    return builder.as_markup()
