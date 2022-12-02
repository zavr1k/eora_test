import pytest

from catbreadbot.bot import BotPhrase, CatBreadBot, Commands, State


def test_create_bot():
    bot = CatBreadBot()
    assert bot.state == State.NONE


transition_cases = [
    (State.NONE, Commands.START[0], State.START,
        f'{BotPhrase.GREETING} {BotPhrase.IS_SQUARE}'),
    (State.NONE, '/fooo', State.NONE, BotPhrase.START),
    (State.START, Commands.NO[0], State.NONE, BotPhrase.CAT),
    (State.START, Commands.YES[0], State.SQUARE, BotPhrase.HAS_EARS),
    (State.START, Commands.START[0], State.START, BotPhrase.IS_SQUARE),
    (State.SQUARE, Commands.YES[0], State.NONE, BotPhrase.CAT),
    (State.SQUARE, Commands.NO[0], State.NONE, BotPhrase.BREAD),
    (State.SQUARE, '', State.SQUARE, BotPhrase.HAS_EARS),
]


@pytest.mark.parametrize(
    "state, message, expected_state, expected_response",
    transition_cases
)
def test_transitions(state, message, expected_state, expected_response):
    bot = CatBreadBot()
    bot._state = state
    response = bot.send(message)

    assert response == expected_response
    assert bot.state == expected_state
