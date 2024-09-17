from aiogram.filters.callback_data import CallbackData


class TaskCallbackFactory(CallbackData, prefix="task"):
    subject_id: int
    task_id: int
    action: str | None


class SolutionCallbackFactory(CallbackData, prefix="solution"):
    solution_id: int
    grade: int


class SupportCallbackFactory(CallbackData, prefix="support"):
    messages: str
    user_id: int
    as_user: bool


class CancelSupportCallbackFactory(CallbackData, prefix="cancel_support"):
    user_id: int
