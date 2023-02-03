from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    KICKED,
    LEFT,
    RESTRICTED,
    MEMBER,
    ADMINISTRATOR,
    CREATOR,
)
from aiogram.types import ChatMemberUpdated
from loader import dp

router = Router()
router.chat_member.filter(F.chat.id == "some id")


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(KICKED | LEFT | RESTRICTED | MEMBER)
        >> (ADMINISTRATOR | CREATOR)
    )
)
async def admin_promoted(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        event.chat.id,
        f"{event.new_chat_member.user.first_name} was changed as admin!",
    )


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(KICKED | LEFT | RESTRICTED | MEMBER)
        << (ADMINISTRATOR | CREATOR)
    )
)
async def admin_demoted(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        event.chat.id,
        f"{event.new_chat_member.user.first_name} was changed as user!",
    )


dp.include_router(router)
