# -*- coding: utf-8 -*-
import pytest

from nameko.testing.services import worker_factory

from .models import Base, PlayerModel
from .services import PlayerService


@pytest.fixture(scope='session')
def model_base():
    return Base


def test_players_model(db_session):
    player = PlayerModel(id=1, name='Joe')
    db_session.add(player)
    db_session.commit()
    saved_player = db_session.query(PlayerModel).get(player.id)
    assert saved_player.id > 0
    assert saved_player.name == 'Joe'


def test_players_service(db_session):

    # create instance, providing the test database session
    service = worker_factory(PlayerService, session=db_session)

    # verify ``save`` logic by querying the test database
    service.create("helloworld")
    assert db_session.query(PlayerModel.name).all() == [("helloworld",)]