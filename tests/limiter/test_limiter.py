import pytest

from engbot.models.words import WordField
from engbot.models.users import UserField
from engbot.database.main_database.repositories.words import CreateWord
from engbot.services.limiters import WordLimiter


@pytest.fixture(scope="module")
def test_data_for_limiter(test_user_data: dict) -> list[dict]:
    data_list = [
        {WordField.ENG_WORD.value: "good", WordField.TRANSlATE.value: "хорошо"},
        {WordField.ENG_WORD.value: "possible", WordField.TRANSlATE.value: "возможный"},
        {WordField.ENG_WORD.value: "record", WordField.TRANSlATE.value: "запись"},
        {WordField.ENG_WORD.value: "tip", WordField.TRANSlATE.value: "совет"},
        {WordField.ENG_WORD.value: "busy", WordField.TRANSlATE.value: "занятый"},
        {WordField.ENG_WORD.value: "here", WordField.TRANSlATE.value: "здесь"},
        {WordField.ENG_WORD.value: "stay", WordField.TRANSlATE.value: "оставаться"},
        {WordField.ENG_WORD.value: "smart", WordField.TRANSlATE.value: "умный"},
        {WordField.ENG_WORD.value: "notice", WordField.TRANSlATE.value: "заметка"},
        {WordField.ENG_WORD.value: "improve", WordField.TRANSlATE.value: "улучшать"},
        {WordField.ENG_WORD.value: "wallet", WordField.TRANSlATE.value: "кошелек"},
    ]
    yield data_list


class TestLimiter:
    def test_limiter_process(
        self, test_data_for_limiter: list[dict], test_user_data: dict
    ):
        telegram_id = test_user_data.get(UserField.TELEGRAM_ID.value)
        between = 2
        # filling database with datas
        for data in test_data_for_limiter[:between]:
            CreateWord(telegram_id, **data)

        limiter = WordLimiter()

        assert limiter.is_acceptable(telegram_id) == True

        for data in test_data_for_limiter[between:]:
            CreateWord(telegram_id, **data)

        assert limiter.is_acceptable(telegram_id) == False
