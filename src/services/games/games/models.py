# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ScalarListType

Base = declarative_base()


class GameModel(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deck_id = Column(Integer)
    player_id = Column(Integer)
    player_hand = Column(ScalarListType(), default=[])
    player_score = Column(Integer, default=0)
    player_ace_high = Column(Boolean, default=False)
    dealer_hand = Column(ScalarListType(), default=[])
    dealer_hand_hidden = Column(ScalarListType(), default=[])
    dealer_score = Column(Integer, default=0)
    dealer_ace_high = Column(Boolean, default=False)
    dealer_ace_high_hidden = Column(Boolean, default=False)

    # Status is an int representing the current game state
    # 0 - Created
    # 1 - PlayerDealt
    #   - No DealerDealt as that would be Ready
    # Game currently playing states:
    # 10 - Ready
    # 11 - Stuck - hidden card revealed here
    # 12 - DealerStuck
    # Winning states:
    # 20 - DealerBust
    # 21 - PlayerWins
    # Losing states:
    # 30 - PlayerBust
    # 31 - DealerWins

    # TODO: status could be an ENUM so it's easier to display.

    status = Column(Integer, default=0)

    def __repr__(self):
        return '<Game(player={!r} status={!r} player_score={!r})>'.format(
            self.player_id, self.status, self.player_score)
