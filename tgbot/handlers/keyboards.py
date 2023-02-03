from random import randint

from aiogram import F, Router
from aiogram.filters import Command, Text
from aiogram.types import CallbackQuery, Message

from loader import bot, dp
from tgbot.keyboards.inline.callbacks import NumbersCallbackFactory
from tgbot.keyboards.inline.keyboard import (
    big_keyboard,
    inline_keyboard,
    random_keyboard,
)
from tgbot.keyboards.reply.example_keyboard import reply_builder
from tgbot.keyboards.reply.special_keyboard import special_buttons

keyboard_router = Router()
keyboard_router.message.filter(F.text)


@keyboard_router.message(Command(commands=["keyboard"]))
async def show_keyboard(message: Message):
    keyboard = reply_builder()
    await message.reply("Your keyboard", reply_markup=keyboard)


@keyboard_router.message(Command(commands=["special_keyboard"]))
async def show_special_keyboard(message: Message):
    keyboard = special_buttons()
    await message.reply("Your keyboard", reply_markup=keyboard)


@keyboard_router.message(Command(commands=["inline"]))
async def show_inline_keyboard(message: Message):
    keyboard = await inline_keyboard(bot)
    await message.reply("Your keyboard", reply_markup=keyboard)


@dp.message(Command(commands=["random"]))
async def show_random_keyboard(message: Message):
    keyboard = random_keyboard()
    await message.reply("Your keyboard", reply_markup=keyboard)


@keyboard_router.message(Command(commands=["big_keyboard"]))
async def show_big_keyboard(message: Message):
    keyboard = big_keyboard()
    await message.reply("Your keyboard", reply_markup=keyboard)


@dp.callback_query(Text(text="random_value"))
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    return await callback.answer(text="Thank you!", show_alert=True)


@keyboard_router.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
async def callbacks_num_change_fab(callback: CallbackQuery):
    await callback.message.answer("Finish")
    return await callback.answer()


@keyboard_router.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callbacks_num_change_fab(
    callback: CallbackQuery, callback_data: NumbersCallbackFactory
):
    await callback.message.answer(callback_data.action + " " + str(callback_data.value))
    return await callback.answer()


@keyboard_router.message(lambda message: int(message.text) in range(16))
async def answer_keyboard(message: Message):
    await message.reply(message.text)


dp.include_router(keyboard_router)
