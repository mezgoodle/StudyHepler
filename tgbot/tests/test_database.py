import pytest

from tgbot.misc.database import Database
from tgbot.models.models import Student, Teacher, close_db, init


@pytest.fixture()
def db():
    return Database()


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests(request):
    await init()
    yield
    await close_db()


# class TestSomething(test.TestCase):
#     async def test_something_async(self, db: Database):
#         teacher = await db.create_teacher(
#             1,
#             "username",
#             "full_name",
#         )
#         assert teacher is not None


@pytest.mark.asyncio
async def test_teacher(db: Database):
    teacher = await db.__create_user(
        Teacher,
        1,
        "username",
        "full_name",
    )
    assert teacher is not None
