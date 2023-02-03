from aiogram.types import KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def special_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Request location", request_location=True),
        KeyboardButton(text="Request contact", request_contact=True),
    )
    builder.row(
        KeyboardButton(
            text="Create a poll", request_poll=KeyboardButtonPollType(type="quiz")
        )
    )
    return builder.as_markup(resize_keyboard=True)
