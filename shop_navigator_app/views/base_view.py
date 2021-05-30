"""
Contains tools for executing CRUD operations with data models
and selecting information about their entities by users via APIs.
"""

from flask_restful import Resource
from flask import request
from sqlalchemy import inspect

from shop_navigator_app import db


class BaseView(Resource):
    """
    Contains methods for getting HTTP-requests and sending HTTP-responses
    to provide APIs to work with application data models.
    """

    def __init__(self, model, schema, service):
        self.model = model
        self.schema = schema()
        self.service = service

    def get(self, instance_id=None):
        """
        :param instance_id: resource identificator to get a specific instance
        :return: if correct instance_id is specified, the function returns the
                 response with instance data that has specified id; if it is
                 not specified, a response with list of all model instances
                 will be returned; if the identificator is wrong, an empty
                 JSON object will be returned
        """
        if instance_id:
            return self.get_single_instance(instance_id)
        model_instances = self.service().get_all_instances(db.session)
        return self.schema.dump(
            model_instances, many=True
        ), 200

    def post(self):
        """
        Creates a table row with the provided data for the model.
        :return: if the correct data passed, a response with
                 the new instance info will be returned;
                 otherwise, a response body will contain an
                 error message
        """
        request_json = request.json
        if not self.check_instance_data(request_json):
            return {'message': 'Incorrect data was passed.'}, 400
        new_instance = self.schema.load(
            request_json, session=db.session
        )
        self.service().insert_new_instance(db.session, new_instance)
        return self.schema.dump(new_instance), 201

    def put(self, instance_id):
        """
        Replaces the instance with specified identificator.
        :param instance_id: resource identificator to get a specific instance
        :return: if the correct data passed, a response with
                 the new instance info will be returned;
                 otherwise, a response body will contain an
                 error message
        """
        model_instance = self.get_model_instance(instance_id)
        if not model_instance:
            return {'message': 'There is no instance with passed id.'}, 404
        request_json = request.json
        if not self.check_instance_data(request_json):
            return {'message': 'Incorrect data was passed.'}, 400
        model_instance = self.schema.load(
            request_json, instance=model_instance,
            session=db.session
        )
        self.service().insert_new_instance(db.session, model_instance)
        return self.schema.dump(model_instance), 200

    def patch(self, instance_id):
        """
        Updates the instance with specified identificator using
        the fields, passed into request body.
        :param instance_id: resource identificator to get a specific instance
        :return: if the correct data passed, a response with
                 the new instance info will be returned;
                 otherwise, a response body will contain an
                 error message
        """
        model_instance = self.service().get_all_instances_by_id(
            db.session, instance_id
        )
        if not model_instance:
            return {}, 404
        updated_data = request.json
        if not self.check_data_to_patch(updated_data):
            return {'message': 'Incorrect data was passed.'}, 400
        self.service.update_instance(
            db.session, model_instance, updated_data
        )
        return self.schema.dump(model_instance), 200

    def delete(self, instance_id):
        """
        Deletes the model instance with the specified identificator.
        :param instance_id: resource identificator to get a specific instance
        :return: a response object
        """
        model_instance = self.get_model_instance(instance_id)
        if not model_instance:
            return {}, 404
        self.service.delete_instance(db.session, model_instance)
        return {}, 204

    def get_single_instance(self, instance_id):
        """
        :param instance_id: resource identificator to get a specific instance
        :return: the HTTP-response with found instance data in case of
        success; otherwise, it contains an empty JSON-object
        """
        model_instance = self.get_model_instance(instance_id)
        if not model_instance:
            return {}, 404
        return self.schema.dump(model_instance), 200

    def get_model_instance(self, instance_id):
        """
        :param instance_id: resource identificator to get a specific instance
        :return: the model instance that has the specified identificator
        """
        return self.service().get_first_instance_by_id(
            db.session, instance_id
        )

    def check_instance_data(self, request_data):
        """
        Checks if all required model data has been passed and
        if there are no extra data.
        :param request_data: client HTTP-request data
        :return: conclusion about the correctness of the passed data
        """
        model_column_set = self.get_model_columns()
        given_column_set = set(request_data.keys())
        return model_column_set == given_column_set

    def check_data_to_patch(self, request_data):
        """
        Checks if the extra data are not passed.
        :param request_data: client HTTP-request data
        :return: conclusion about the correctness of the passed data
        """
        model_column_set = self.get_model_columns()
        given_column_set = set(request_data.keys())
        return given_column_set.issubset(model_column_set)

    def get_model_columns(self):
        """
        :return: a set of the columns that the model contains
        """
        model_column_set = set(
            inspect(self.model).column_attrs.keys()
        )
        model_column_set.remove('id')
        return model_column_set
