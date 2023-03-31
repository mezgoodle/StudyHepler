from pathlib import Path

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentTypes, InputFile, Message

from loader import dp
from tgbot.misc.import_students import parse_students_from_file
from tgbot.misc.utils import check_extension, delete_file, download_file
from tgbot.models.database import Database


@dp.message_handler(Command(["register_teacher"]))
async def register_teacher(message: Message) -> Message:
    db: Database = message.bot.get("db")
    user = message.from_user
    if db.get_teacher(message.from_user.id):
        return await message.answer("You are already registered as teacher")
    if db.create_teacher(
        name=user.full_name, telegram_id=user.id, username=user.username
    ):
        return await message.answer("You are registered as teacher")
    return await message.answer("Something went wrong")


@dp.message_handler(Command(["add_students"]))
async def add_students(message: Message, state: FSMContext) -> Message:
    await state.set_state("wait_for_file")
    path_to_file = Path().joinpath("files", "exports", "example.xlsx")
    await message.answer_document(InputFile(path_to_file), caption="Example")
    return await message.answer(
        "Send file with students' data as in the example. Formats: .csv, .xlsx, .xls"
    )


@dp.message_handler(state="wait_for_file", content_types=ContentTypes.DOCUMENT)
async def process_file(message: Message, state: FSMContext) -> Message:
    await state.finish()
    if message.document:
        try:
            file_name = message.document.file_name
            check_extension(file_name)
            downloaded_path = await download_file(file_name, message)
            db = message.bot.get("db")
            parse_students_from_file(downloaded_path, db)
            delete_file(downloaded_path)
        except Exception as error_message:
            return await message.answer(error_message)
        return await message.answer("Students were added")
    return await message.answer(
        "You should send file with students' data. Formats: .csv, .xlsx, .xls"
    )
