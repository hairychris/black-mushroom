""" Service integration testing best practice.
"""
from nameko.testing.utils import get_container
from nameko.testing.services import entrypoint_hook

from black_mushroom.decks.services import DeckService
from black_mushroom.games.services import GameService


def test_service_game_deck_integration(runner_factory, rabbit_config):

    # run services in the normal manner
    runner = runner_factory(rabbit_config, GameService, DeckService)
    runner.start()

    # artificially fire the "create" entrypoint on GameService
    container = get_container(runner, GameService)
    with entrypoint_hook(container, "create") as entrypoint:
        # TODO: fix assert, this will only work on first run.
        assert entrypoint("Joe").player_id == 1
