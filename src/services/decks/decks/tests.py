# -*- coding: utf-8 -*-
import pytest

from .models import Base, DeckModel


@pytest.fixture(scope='session')
def model_base():
    return Base


def test_decks(db_session):
    deck = DeckModel(id=1)
    db_session.add(deck)
    db_session.commit()
    saved_deck = db_session.query(DeckModel).get(deck.id)
    assert saved_deck.id > 0
