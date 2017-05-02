# -*- coding: utf-8 -*-
"""Services that relate to a game of cards, reusable for other projects.

This module was built to handle a 52 card game of playing cards.

Example:
    To run the game related services on their own::

        $ nameko run black_mushroom.games.services --config config.yml

Todo:
    * Consider adding delete, cascade delete may be more appropriate.
"""

import logging
from nameko.rpc import rpc, RpcProxy
from nameko_sqlalchemy import DatabaseSession

from black_mushroom.base.services import BaseService

from .models import Base, GameModel
from .schemas import GameSchema, GameSchemaStuck

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)


class GameService(BaseService):
    """Provides a Nameko service to handle card game activities.

    This service has external service dependencies. It depends on

        1. PlayerService
        2. DeckService

    Attributes:
        name (str): Service name for Nameko
        model (cls): Primary model for this particular service
        schema (cls): Main marshmallow schema class for this service
        session (DataseSession): SQLAlchemy session

        player_rpc (RpcProxy(PlayerService)): users / players
        deck_rpc (RpcProxy(DeckService)): deck of cards
        
        player_cards (int): no. of cards for player at start
        dealer_cards (int): no. of visible cards for dealer at start
        dealer_cards_hidden (int): no. hidden cards for dealer at start

    """

    name = "game"
    model = GameModel
    schema = GameSchema
    session = DatabaseSession(Base)

    # we depend on these RPC interface.
    player_rpc = RpcProxy("player")
    deck_rpc = RpcProxy("deck")

    # TODO: move these variables into the config file using plugin.
    player_cards = 2
    dealer_cards = 1
    dealer_cards_hidden = 1

    def _setup_game(self, model):
        if not (self.dealer_cards + self.dealer_cards_hidden) == 2:
            # TODO: don't use generic exception, use ValueError or better.
            raise Exception('The dealer must have exactly two cards.')
        if not (self.player_cards == 2):
            # TODO: don't use generic exception, use ValueError or better.
            raise Exception('The player must have exactly two cards.')
        # When the game starts, the player is given 2 random cards
        for i in range(1, self.player_cards + 1):
            self._hit(model)
        model.status = 1
        self.update_model(model)
        # The dealer is given 0 or more card(s) that are hidden.
        for i in range(1, self.dealer_cards + 1):
            self._hit(model, hidden=False)
        # The dealer is given 0 or more card(s) that are visible.
        for i in range(1, self.dealer_cards_hidden + 1):
            self._hit(model, hidden=True)
        model.status = 10
        self.update_model(model)

    def _get_score(self, hand):
        score = 0
        for card in hand:
            points = int(card[1:])
            if points > 10:
                points = 10
            score += points
        return score

    def _check(self, model):
        # TODO: refactor this into check, check_player and check_dealer

        # We are checking for a player
        if model.status == 0 or model.status == 10:
            model.player_score = self._get_score(model.player_hand)
            # PlayerBlackjack
            if model.player_score == 21:
                model.status = 21
            # PlayerBust
            if model.player_score > 21:
                model.status = 30
        # We are checking for a dealer
        elif model.status == 1 or model.status == 11:
            model.dealer_score = self._get_score(
                model.dealer_hand_hidden + model.dealer_hand)
            # TODO: check player_score is set here.
            # TODO: check if dealer_score is greater than player_score
            # DealerWins
            if model.dealer_score == 21:
                model.status = 31
            # DealerBust
            if model.dealer_score > 21:
                model.status = 30
        else:
            raise(ValueError(
                'The game has an unknown status: {}'.format(model.status)))
        return model

    def _hit(self, model, hidden=None):
        # Hidden - True for dealing hidden dealer card, False for shown dealer
        # card, None for player card
        deck_id = model.deck_id
        # TODO: check if we should be dealing a card or this one will
        # get thrown away after we throw an error.
        card = self.deck_rpc.deal_card(deck_id)

        # It is the dealers turn.
        if model.status == 1 or model.status == 11:
            # TODO: be careful, we remove a card from the deck before putting
            # it in a hand, we could lose the card if we throw an error.
            if hidden:
                hand = list(model.dealer_hand_hidden)
                hand.append(card)
                model.dealer_hand_hidden = hand
            else:
                hand = list(model.dealer_hand)
                hand.append(card)
                model.dealer_hand = hand
        # It is the players turn.
        elif model.status == 0 or model.status == 10:
            # TODO: be careful, we remove a card from the deck before putting
            # it in a hand, we could lose the card if we throw an error.
            hand = list(model.player_hand)
            hand.append(card)
            model.player_hand = hand
        # User has stuck, don't let them fetch any more cards.
        elif model.status in [11, 12]:
            # We are stuck, we don't need to update anything.
            return None
        else:
            raise NotImplementedError(
                'Implement _hit for status: {}'.format(model.status))

        # Check that model has been saved, if it has we can run _check()
        model = self._check(model)
        self.update_model(model)
        return model

    def _toggle_ace(self, model, dealer=False):
        hand = None
        if dealer:
            # iterate through dealer cards hidden
            for card in model.dealer_hand_hidden:
                if int(card[1:]) == 1:
                    # we have an ace
                    # TODO: add code to ensure we can't end up with two aces
                    # high as that is insta-bust
                    model.dealer_ace_high_hidden ^= True
                    hand = list(self.dealer_hand_hidden)
                    model.dealer_hand = hand
            # iterate through dealer cards
            for card in model.dealer_hand:
                if int(card[1:]) == 1:
                    # we have an ace
                    # TODO: add code to ensure we can't end up with two aces
                    # high as that is insta-bust
                    model.dealer_ace_high ^= True
                    hand = list(self.dealer_hand)
                    model.dealer_hand = hand
        else:
            # iterate through user cards
            for card in model.player_hand:
                if int(card[1:]) == 1:
                    # we have an ace
                    model.player_ace_high = not model.player_ace_high
                    hand = list(self.player_hand)
                    model.player_hand = hand
        model = self.check(model)
        self.update_model(model)
        return model

    @rpc
    def create(self, player_id=None):
        """Creates model objects.

        Args:
            player_id (int): The foreign key for player.

        Returns:
            int: primary key of created model

        """

        # TODO: check player_id exists.
        logging.debug('GameService.create({})'.format(player_id))
        player = self.player_rpc.get(player_id)
        print(player)
        if player:
            # create a deck whenever we create a game.
            model = self.create_model(
                player_id=player['id'],
                deck_id=self.deck_rpc.create()['id'],
                status=0,  # Status: Created.
            )
            self._setup_game(model)
            return self.schema().dump(model).data
        else:
            # TODO: exception handling, how to pass errors?
            raise Exception(
                'Player with id={} does not exist'.format(player_id))

    @rpc
    def get(self, id):
        """Creates model objects.

        Args:
            id (int): The primary key of the fetched model.

        Returns:
            GameModel: SQLAlchemy model if exists, False otherwise

        """

        return self.schema().dump(self.get_model(id)).data

    @rpc
    def hit(self, id):
        model = self.get_model(id)
        if model.status == 10:
            return self.schema().dump(self._hit(model)).data
        else:
            # TODO: check status and return appropriate error message.
            return False

    @rpc
    def toggle_ace(self, id):
        model = self.get_model(id)
        return self.schema().dump(self._toggle_ace(model)).data

    @rpc
    def stick(self, id):
        # TODO: refactor stick into _stick
        model = self.get_model(id)
        if model.status == 10:
            model.status = 11
            self.update_model(model)
            while True:
                if (model.player_score > 21):
                    print('PlayerBust')
                    model.status = 30
                    break
                elif model.dealer_score > 21:
                    print('DealerBust')
                    model.status = 20
                    break
                elif model.status == 12:
                    print('DealerWins')
                    model.status = 31
                    break
                elif model.dealer_score == 21:
                    print('DealerStuck')
                    model.status = 12
                elif model.dealer_score > model.player_score:
                    print('DealerStuck')
                    model.status = 12
                # The player can't win outright as dealer won't stick until
                # they win.
                print('DealerHit')
                self._hit(model)
            self.update_model(model)

            # reveal the dealers card by setting exclude to blank.
            return GameSchemaStuck().dump(model).data
        else:
            # TODO: check status and return appropriate error message.
            return False
