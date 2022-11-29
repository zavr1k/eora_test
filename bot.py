from enum import Enum, auto
from typing import Union


class State(Enum):
    NONE = auto()
    START = auto()
    SQUARE = auto()


class BotPhrase:
    GREETING = 'Привет! Я могу отличить кота от хлеба.'

    CAT = 'Это кот а не хлеб! Не ешь его!'
    BREAD = 'Это хлеб, а не кот. Ешь его!'

    HAS_EARS = 'У него есть уши?'
    IS_SQUARE = 'Объект перед тобой квадратный?'


class CatBreadBot:

    _start = ('/start',)
    _yes = ('да', 'конечно', 'ага', 'пожалуй', 'yes')
    _no = ('нет', 'нет,конечно', 'ноуп', 'найн', 'no')

    def __init__(self, user_id: Union[str, int, None] = None) -> None:
        self.user_id = user_id
        self._state = State.NONE
        self._user_message = None

    @property
    def state(self) -> State:
        return self._state

    def __repr__(self) -> str:
        return f"CatBreadBot(user_id={self.user_id}, state={self.state})"

    def reset_state(self) -> None:
        self._state = State.NONE
        self._user_message = None

    def say(self, message: str) -> str | None:
        self._user_message = message.lower().strip()

        if self.state is State.NONE:
            return self._start_handler()
        elif self.state is State.START:
            return self._square_handler()
        elif self.state is State.SQUARE:
            return self._ear_handler()

    def _start_handler(self) -> str | None:
        if self._user_message in self._start:
            self._state = State.START
            return f'{BotPhrase.GREETING} {BotPhrase.IS_SQUARE}'

    def _square_handler(self) -> str | None:
        if self._user_message in self._yes:
            self._state = State.SQUARE
            return BotPhrase.HAS_EARS
        elif self._user_message in self._no:
            self.reset_state()
            return BotPhrase.CAT

    def _ear_handler(self) -> str | None:
        if self._user_message in self._yes:
            self.reset_state()
            return BotPhrase.CAT
        elif self._user_message in self._no:
            self.reset_state()
            return BotPhrase.BREAD
