from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
    ADMINISTRATOR,
)
from aiogram.types import ChatMemberUpdated
from loader import dp

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR)
)
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):

    await bot.send_message(
        chat_id=event.chat.id,
        text=f"Hello! Thank you for adding me in "
        f'{event.chat.type} "{event.chat.title}" '
        f"as administrator. ID chat: {event.chat.id}",
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER)
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await bot.send_message(
            chat_id=event.chat.id,
            text=f"Hi! Thank you for adding me in "
            f'{event.chat.type} "{event.chat.title}" '
            f"as member. ID chat: {event.chat.id}",
        )
    else:
        print("Eror")


dp.include_router(router)
