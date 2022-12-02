from enum import StrEnum, auto


class State(StrEnum):
    NONE = auto()
    START = auto()
    SQUARE = auto()


class BotPhrase:
    GREETING = 'Привет! Я могу отличить кота от хлеба.'
    START = 'Для запуска бота введите команду /start'

    CAT = 'Это кот а не хлеб! Не ешь его!'
    BREAD = 'Это хлеб, а не кот. Ешь его!'
    NOTHING_TO_SAY = 'Мне нечего на это ответить'

    HAS_EARS = 'У него есть уши?'
    IS_SQUARE = 'Объект перед тобой квадратный?'


class Commands:
    START = ('/start',)
    YES = ('да', 'конечно', 'ага', 'пожалуй', 'yes')
    NO = ('нет', 'нет,конечно', 'ноуп', 'найн', 'no')


class CatBreadBot:

    def __init__(self) -> None:
        self._state = State.NONE
        self._user_message = None

    @property
    def state(self) -> State:
        return self._state

    def __repr__(self) -> str:
        return f"CatBreadBot(state={self.state})"

    def reset_state(self) -> None:
        self._state = State.NONE
        self._user_message = None

    def send(self, message: str) -> str:
        self._user_message = message.lower().strip()

        if self.state is State.NONE:
            return self._start_handler()
        elif self.state is State.START:
            return self._square_handler()
        elif self.state is State.SQUARE:
            return self._ear_handler()

        return BotPhrase.NOTHING_TO_SAY

    def _start_handler(self) -> str:
        if self._user_message in Commands.START:
            self._state = State.START
            return f'{BotPhrase.GREETING} {BotPhrase.IS_SQUARE}'
        return BotPhrase.START

    def _square_handler(self) -> str:
        if self._user_message in Commands.YES:
            self._state = State.SQUARE
            return BotPhrase.HAS_EARS
        elif self._user_message in Commands.NO:
            self.reset_state()
            return BotPhrase.CAT
        return BotPhrase.IS_SQUARE

    def _ear_handler(self) -> str:
        if self._user_message in Commands.YES:
            self.reset_state()
            return BotPhrase.CAT
        elif self._user_message in Commands.NO:
            self.reset_state()
            return BotPhrase.BREAD

        return BotPhrase.HAS_EARS
