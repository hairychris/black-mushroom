# -*- coding: utf-8 -*-
"""Services that relate to a game player, reusable for other projects.

This module was built to handle a super simple player, it should really
handle authentication as well but it does not at the moment.

Example:
    To run the player related services on their own::

        $ nameko run black_mushroom.players.services --config config.yml

Todo:
    * Consider adding delete, cascade delete may be more appropriate.
    * Add some sort of authentication even if it's just token based.
    * Eventually add JWT support, should be in a new service.
"""

from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession

from black_mushroom.base.services import BaseService

from .models import Base, PlayerModel
from .schemas import PlayerSchema


class PlayerService(BaseService):
    """Provides a Nameko service to handle game player activities.

    This service does not have any external service dependencies.

    Attributes:
        name (str): Service name for Nameko
        model (cls): Primary model for this particular service

    """

    name = "player"
    model = PlayerModel
    schema = PlayerSchema
    session = DatabaseSession(Base)

    @rpc
    def create(self, name):
        """Creates model objects.

        Args:
            name (int): The name of the player.

        Returns:
            dict: created model as dictionary via marshmallow schema.

        """

        model = self.create_model(name=name)
        return self.schema().dump(model).data

    @rpc
    def get(self, id):
        """Creates model objects.

        Args:
            id (int): The primary key of the fetched model.

        Returns:
            dict: model dictionary if exists, False otherwise.

        """

        return self.schema().dump(self.get_model(id)).data

    @rpc
    def filter(self, **kwargs):
        """Filters model objects by keys and serializes the result.

        Args:
            id (int): The primary key of the fetched model.

        Returns:
            dict: list of model dictionaries if exists, False otherwise.

        """
        # TODO: error handling
        return self.schema(many=True).dump(self.filter_model(**kwargs)).data

    @rpc
    def update(self, raw_obj, many=False):
        """Updates model objects with keys and serializes the result.

        Args:
            id (int): The primary key of the fetched model.

        Returns:
            dict: list of model dictionaries if exists, False otherwise.

        """
        # TODO: catch and handle malformed schema errors.
        model = self.schema(many=many).load(raw_obj).data
        return self.schema().dump(self.update_model(model)).data
