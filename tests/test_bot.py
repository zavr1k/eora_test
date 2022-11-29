import pytest

from bot import BotPhrase, CatBreadBot, State


def test_create_bot():
    bot = CatBreadBot(1)
    assert bot.state == State.NONE
    assert bot.user_id == 1


transition_cases = [
    (State.NONE, '/start', State.START,
        f'{BotPhrase.GREETING} {BotPhrase.IS_SQUARE}'),
    (State.START, 'no', State.NONE, BotPhrase.CAT),
    (State.START, 'yes', State.SQUARE, BotPhrase.HAS_EARS),
    (State.SQUARE, 'yes', State.NONE, BotPhrase.CAT),
    (State.SQUARE, 'no', State.NONE, BotPhrase.BREAD),
]


@pytest.mark.parametrize(
    "state, message, expected_state, expected_response",
    transition_cases
)
def test_transitions(state, message, expected_state, expected_response):
    bot = CatBreadBot()
    bot._state = state
    response = bot.say(message)

    assert response == expected_response
    assert bot.state == expected_state
