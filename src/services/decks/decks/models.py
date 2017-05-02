from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ScalarListType

Base = declarative_base()


class DeckModel(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    face_down_cards = Column(ScalarListType(), default=[])
    dealt_cards = Column(ScalarListType(), default=[])

    def __repr__(self):
        return '<Deck(face_down_cards={!} dealt_cards={!r})>'.format(
            self.face_down_cards, self.dealt_cards)
