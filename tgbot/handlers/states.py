available_food_names = ["Sushi", "Spagetti", "Cake"]
available_food_sizes = ["Mini", "Medium", "Big"]

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from tgbot.keyboards.reply.state_keyboard import make_row_keyboard
from tgbot.states.states import OrderFood

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message(Command(commands=["food"]))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Choose food:", reply_markup=make_row_keyboard(available_food_names)
    )
    await state.set_state(OrderFood.choosing_food_name)


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Thank you. Now choose a size:",
        reply_markup=make_row_keyboard(available_food_sizes),
    )
    await state.set_state(OrderFood.choosing_food_size)


@router.message(OrderFood.choosing_food_name)
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know such a meal.\n\n" "Please, choose onw from the keyboard:",
        reply_markup=make_row_keyboard(available_food_names),
    )


@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"You have chosen {message.text.lower()} of {user_data['chosen_food']}.\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know such a meal.\n\n" "Please, choose onw from the keyboard:",
        reply_markup=make_row_keyboard(available_food_sizes),
    )


dp.include_router(router)
