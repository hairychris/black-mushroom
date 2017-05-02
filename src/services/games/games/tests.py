# -*- coding: utf-8 -*-
import pytest

# TODO: we should mock these so we don't have a depdency
from black_mushroom.decks.models import DeckModel
from black_mushroom.players.models import PlayerModel

from .models import Base, GameModel


@pytest.fixture(scope='session')
def model_base():
    return Base


def test_games(db_session):
    game = GameModel(id=1)
    db_session.add(game)
    db_session.commit()
    saved_game = db_session.query(GameModel).get(game.id)
    assert saved_game.id > 0
