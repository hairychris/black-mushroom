from marshmallow_sqlalchemy import ModelSchema

from .models import GameModel


class GameSchema(ModelSchema):
    class Meta:
        model = GameModel
        exclude = (
            'deck_id',
            'dealer_score',
            'dealer_hand_hidden',
            'dealer_ace_high_hidden'
        )


class GameSchemaStuck(ModelSchema):
    class Meta:
        model = GameModel
        exclude = ('deck_id',)
