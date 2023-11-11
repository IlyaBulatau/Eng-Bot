from aiohttp import ClientSession

from enum import Enum
from contextlib import asynccontextmanager


TRANSLATE_API_URL = (
    "https://ftapi.pythonanywhere.com/translate?sl={sl}&dl={dl}&text={text}"
)


class LanguageCodeEnum(Enum):
    ENGLISH: str = "en"
    RUSSIAN: str = "ru"


class Translator:
    """
    Makes request to API of translate
    and get result of the request
    """

    def __init__(
        self,
        sl: str = LanguageCodeEnum.ENGLISH.value,
        dl: str = LanguageCodeEnum.RUSSIAN.value,
    ) -> None:
        self.format_url: str = TRANSLATE_API_URL
        self.sl: str = sl
        self.dl: str = dl
        self.translate_text_key = "destination-text"
        self.translate_possible_key = ("translations", "possible-translations")
        self.pronunciation_keys = ("pronunciation", "destination-text-audio")

    @asynccontextmanager
    async def get_session(self, url: str):
        async with ClientSession() as client:
            async with client.get(url) as session:
                yield session
                session.close()

    async def translate(self, text: str) -> tuple[str, list[str], str]:
        """
        Returns tuple of 3 object
        First - some translate result
        Second - list of other translation
        Third - link on pronunciation of word
        """
        url = self.format_url.format(sl=self.sl, dl=self.dl, text=text)

        async with self.get_session(url) as session:
            response: dict = await session.json()

        return self._parse_data(response)

    def _parse_data(self, response: dict) -> tuple[str, list[str], str]:
        """
        Parses data from response
        """
        translate_text: str = response.get(self.translate_text_key, None)

        possible_translate: list[str] = (
            key.get(self.translate_possible_key[1], None)
            if (key := response.get(self.translate_possible_key[0], None))
            else None
        )

        pronociation_translate: str = (
            key.get(self.pronunciation_keys[1])
            if (key := response.get(self.pronunciation_keys[0], None))
            else None
        )

        return (translate_text, possible_translate, pronociation_translate)
