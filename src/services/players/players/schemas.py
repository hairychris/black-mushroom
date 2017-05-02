from marshmallow_sqlalchemy import ModelSchema

from .models import PlayerModel


class PlayerSchema(ModelSchema):
    class Meta:
        model = PlayerModel
