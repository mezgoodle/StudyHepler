from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentTypes, Message

from loader import dp
from tgbot.misc.import_students import parse_students_from_file
from tgbot.misc.utils import check_extension, download_file


@dp.message_handler(Command(["add_students"]))
async def add_students(message: Message, state: FSMContext) -> Message:
    await state.set_state("wait_for_file")
    # TODO: send template file
    return await message.answer(
        "Send file with students' data. Formats: .csv, .xlsx, .xls"
    )


@dp.message_handler(state="wait_for_file", content_types=ContentTypes.DOCUMENT)
async def process_file(message: Message, state: FSMContext) -> Message:
    await state.finish()
    if message.document:
        try:
            file_name = message.document.file_name
            check_extension(file_name)
            downloaded_path = await download_file(file_name, message)
            parse_students_from_file(downloaded_path)
        except Exception as error_message:
            return await message.answer(error_message)
        return await message.answer("Students were added")
    return await message.answer(
        "You should send file with students' data. Formats: .csv, .xlsx, .xls"
    )
