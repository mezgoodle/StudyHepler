from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import dp
from tgbot.filters.student import IsStudentFilter
from tgbot.keyboards.inline.callbacks import TaskCallbackFactory
from tgbot.misc.database import Database
from tgbot.models.models import Student
from tgbot.states.states import Solution

router = Router()
router.message.filter(IsStudentFilter())
router.callback_query.filter(IsStudentFilter())
dp.include_router(router)


@router.callback_query(TaskCallbackFactory.filter(F.action == "create"))
async def create_solution(
    callback: CallbackQuery,
    callback_data: TaskCallbackFactory,
    state: FSMContext,
    student: Student,
) -> Message:
    await state.set_state(Solution.file_link)
    await state.update_data(
        {"subject_id": callback_data.subject_id, "student_id": student.id}
    )
    return await callback.answer("Task created")


@router.message(Solution.file_link, F.document)
async def set_solution_file_link(
    message: Message, state: FSMContext, db: Database, bot: Bot
) -> Message:
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, message.document.file_name)
    await state.update_data(file_link=message.text)
    data = await state.get_data()
    await state.clear()
    await db.create_solution(**data)
    return await message.answer("Write a task id")
