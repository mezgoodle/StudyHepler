from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.filters.admin import IsAdminFilter

router = Router()
router.message.filter(IsAdminFilter(353057906))
dp.include_router(router)


@router.message(Command("admin"))
async def command_admin_handler(message: Message) -> None:
    return await message.answer("You are admin!")
