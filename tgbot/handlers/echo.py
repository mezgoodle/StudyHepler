# Example: https://docs.aiogram.dev/en/dev-3.x/dispatcher/router.html


from datetime import datetime

from aiogram import F, Router, html
from aiogram.filters import Command, CommandObject, CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp

echo_router = Router()
echo_router.message.filter(F.text)


@echo_router.message(CommandStart())
async def answer_start(message: Message):
    return await message.answer("This is start")


@echo_router.message(Command(commands=["cancel"]))
@echo_router.message(Text(text="cancel", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Action is canceled", reply_markup=ReplyKeyboardRemove())


@echo_router.message(Command(commands=["custom", "custom1"]))
async def answer_custom_command(message: Message):
    return await message.answer("This is custom command")


@echo_router.message(Command(commands=["name"]))
async def answer_name(message: Message, command: CommandObject):
    if command.args:
        return await message.reply(f"Hello, {html.quote(command.args)}")
    return await message.answer("No name")


@dp.message(Command(commands=["entities"]))
async def extract_data(message: Message):
    data = {"url": "<N/A>", "email": "<N/A>", "code": "<N/A>"}
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    return await message.reply(
        "I have found:\n"
        f"URL: {html.quote(data['url'])}\n"
        f"E-mail: {html.quote(data['email'])}\n"
        f"Password: {html.quote(data['code'])}"
    )


@dp.message(F.animation)
async def echo_gif(message: Message):
    return await message.reply_animation(message.animation.file_id)


@dp.message(F.new_chat_members)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        await message.reply(f"Привет, {user.full_name}")


@echo_router.message()
async def echo_with_time(message: Message):
    time_now = datetime.now().strftime("%H:%M")
    added_text = html.underline(f"Created in {time_now}")
    return await message.answer(f"{message.html_text}\n\n{added_text}")


dp.include_router(echo_router)
