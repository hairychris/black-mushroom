# -*- coding: utf-8 -*-
"""Base service for all other services.

This module provides helpers to access database via session

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

"""


class BaseService:

    def filter_model(self, **kwargs):
        return self.session.query(self.model).filter(**kwargs)

    def get_model(self, id):
        model = self.session.query(self.model).get(id)
        return model

    def create_model(self, **kwargs):
        # application logic goes here
        obj = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        return obj

    def update_model(self, new_model):
        # TODO: check if current_model exists.
        # TODO: consider adding get_or_update function here,
        model = self.get_model(new_model['id'])
        for key, value in new_model.iteritems():
            setattr(model, key, value)
        self.session.add(model)
        self.session.commit()
        return model
