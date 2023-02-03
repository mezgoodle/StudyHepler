from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.filters.chat_type import ChatTypeFilter
from tgbot.filters.usernames import HasUsernamesFilter

filter_router = Router()
filter_router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


@filter_router.message(Command(commands=["dice"]))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji="🎲")


@filter_router.message(Command(commands=["basketball"]))
async def cmd_basketball_in_group(message: Message):
    await message.answer_dice(emoji="🏀")


@filter_router.message(
    HasUsernamesFilter(),
)
async def message_with_usernames(message: Message, usernames: List[str]):
    await message.answer(f"Founded usernames: " f'{", ".join(usernames)}')


dp.include_router(filter_router)
