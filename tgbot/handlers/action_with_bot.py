# Example: https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/magic_filters.html

from aiogram import F, Router
from aiogram.filters.chat_member_updated import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.filters.command import Command, CommandStart
from aiogram.types import ChatMemberUpdated, Message

from loader import dp

router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")

users = {111, 222}


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    users.discard(event.from_user.id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    users.add(event.from_user.id)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello")
    users.add(message.from_user.id)


@router.message(Command(commands="users"))
async def cmd_users(message: Message):
    await message.answer("\n".join(f"• {user_id}" for user_id in users))


dp.include_router(router)
