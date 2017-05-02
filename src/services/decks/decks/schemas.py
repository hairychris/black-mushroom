from marshmallow_sqlalchemy import ModelSchema

from .models import DeckModel


class DeckSchema(ModelSchema):
    class Meta:
        model = DeckModel
        exclude = ('face_down_cards',)
