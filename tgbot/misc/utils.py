import logging
import os
from json import dumps

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hbold, hlink

from loader import bot
from tgbot.keyboards.inline.task_keyboard import task_keyboard
from tgbot.misc.database import Database
from tgbot.models.models import Subject
from tgbot.states.states import Task


async def create_subject_message(
    subjects: list[Subject],
    methods: list[dict[str, str]],
) -> str:
    rows = []
    for subject in subjects:
        links = []
        for method in methods:
            links.append(
                hlink(
                    method.get("text"),
                    await create_link(subject.id, method.get("name")),
                )
            )
        rows.append(f"{subject.id}. {subject.name}. {', '.join(links)}")

    return "\n".join(rows)


async def create_link(subject_id: int, key: str) -> str:
    return await create_start_link(
        bot, dumps({"key": key, "id": subject_id}), True
    )


async def add_student_to_subject(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.add(student)
        return await message.answer(
            f'You are now a student of "{subject.name}"'
        )
    return await message.answer("Subject or student not found")


async def quit_student_to_subject(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.remove(student)
        return await message.answer(
            f'You are now not a student of "{subject.name}"'
        )
    return await message.answer("Subject or student not found")


async def see_tasks(
    message: Message,
    payload: dict,
    db: Database,
    *args,
    **kwargs,
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        tasks := await subject.tasks
    ):
        await message.answer("Here are your tasks")
        for task in tasks:
            await message.answer(
                f"{hbold('Name')}: {task.name}\n"
                f"{hbold('Description')}: {task.description}\n"
                f"{hbold('Due date')}: {task.due_date}",
                reply_markup=await task_keyboard(
                    subject.id, task.id, message.from_user.id, db
                ),
            )
        return await message.answer("Your buttons depend on your role")
    return await message.answer("There are no tasks in this subject")


async def add_task(
    message: Message,
    payload: dict,
    db: Database,
    state: FSMContext,
    *args,
    **kwargs,
) -> str:
    if (
        (subject := await db.get_subject(payload.get("id")))
        and (teacher := await subject.teacher)
        and teacher.user_id == message.from_user.id
    ):
        await state.set_state(Task.name)
        await state.update_data(subject_id=subject.id)
        return await message.answer("Write a name for task")
    return await message.answer("You are not a teacher of this subject")


def delete_file(file_path: str):
    try:
        os.remove(file_path)
        logging.info(f"File {file_path} has been deleted successfully locally")
    except FileNotFoundError:
        logging.error(f"The file {file_path} does not exist")
    except PermissionError:
        logging.error(f"Permission denied: unable to delete {file_path}")
    except OSError as e:
        logging.error(f"Error: {e}")


utils = {
    "add_subject": add_student_to_subject,
    "quit_subject": quit_student_to_subject,
    "add_task": add_task,
    "see_tasks": see_tasks,
}
