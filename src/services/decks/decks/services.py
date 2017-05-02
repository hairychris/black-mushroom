# -*- coding: utf-8 -*-
"""Services that relate to a deck of cards, reusable for other projects.

This module was built to handle a 52 card deck of playing cards.

Example:
    To run the deck related services on their own::

        $ nameko run black_mushroom.decks.services --config config.yml

Todo:
    * Consider adding delete, cascade delete may be more appropriate.
"""

import random

from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession

from black_mushroom.base.services import BaseService

from .models import Base, DeckModel
from .schemas import DeckSchema


class DeckService(BaseService):
    """Provides a Nameko service to handle card deck activities.

    This service does not have any external service dependencies.

    Attributes:
        name (str): Service name for Nameko
        model (cls): Primary model for this particular service

    """

    name = "deck"
    model = DeckModel
    schema = DeckSchema
    session = DatabaseSession(Base)

    @rpc
    def create(self):
        """Creates a standard set of 52 cards

        H - hearts, D - diamonds, C - clubs, S - suits

        Returns:
            int: primary key of created model

        """

        suits = ['H', 'D', 'C', 'S']
        cards = []
        # Generate all 4 suits
        for suit in suits:
            # Generate 13 cards per suit
            for i in range(1, 14):
                # Face cards are numbered, convert to points later.
                cards.append('{}{}'.format(suit, i))
        # Let's shuffle these cards.
        # TODO: when containerising via docker make sure we have a
        # decent source of random or this won't be properly random.
        random.shuffle(cards)
        model = self.create_model(face_down_cards=cards)
        return self.schema().dump(model).data

    @rpc
    def get(self, id):
        """Creates model objects.

        Args:
            id (int): The primary key of the fetched model.

        Returns:
            DeckModel: SQLAlchemy model if exists, False otherwise

        """
        data = self.schema(self.get_model(id)).dump().data
        return data

    @rpc
    def deal_card(self, id):
        model = self.get_model(id)

        # TODO: This is disgusting, we copy the whole list however
        # SQLAlchemy was fighting me and this is a tech demo so I decided
        # to find another path, am I happy? No. Does it work? Yes.
        face_down_cards = list(model.face_down_cards)
        dealt_cards = list(model.dealt_cards)

        # Pop from the start of the deck.
        card = face_down_cards.pop(0)

        # TODO: add error handling when we reach the end of the deck
        # which should actually never occur in blackjack.
        dealt_cards.append(card)

        # TODO: remove list copy hack
        model.face_down_cards = face_down_cards
        model.dealt_cards = dealt_cards
        self.update_model(model)
        return card
