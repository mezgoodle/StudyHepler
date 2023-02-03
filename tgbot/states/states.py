# Example: https://docs.aiogram.dev/en/dev-3.x/dispatcher/finite_state_machine/index.html

from aiogram.fsm.state import State, StatesGroup


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()
