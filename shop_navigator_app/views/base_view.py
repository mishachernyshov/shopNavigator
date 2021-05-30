from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import inspect

from shop_navigator_app import db


class BaseView(Resource):
    def __init__(self, model, schema, service):
        self.model = model
        self.schema = schema()
        self.service = service

    def get(self, id=None):
        if id:
            return self.get_single_instance(id)
        model_instances = self.service().get_all_instances(db.session)
        return self.schema.dump(
            model_instances, many=True
        ), 200

    def post(self):
        request_json = request.json
        if not self.check_instance_data(request_json):
            return {'message': 'Incorrect data was passed.'}, 400
        new_instance = self.schema.load(
            request_json, session=db.session
        )
        self.service().insert_new_instance(db.session, new_instance)
        return self.schema.dump(new_instance), 201

    def put(self, id):
        model_instance = self.get_model_instance(id)
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

    def patch(self, id):
        model_instance = self.service().get_all_instances_by_id(
            db.session, id
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

    def delete(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return {}, 404
        self.service.delete_instance(db.session, model_instance)
        return {}, 204

    def get_single_instance(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return {}, 404
        return self.schema.dump(model_instance), 200

    def get_model_instance(self, id):
        return self.service().get_first_instance_by_id(db.session, id)

    def check_instance_data(self, request_data):
        model_column_set = self.get_model_columns()
        given_column_set = set(request_data.keys())
        return model_column_set == given_column_set

    def check_data_to_patch(self, request_data):
        model_column_set = self.get_model_columns()
        given_column_set = set(request_data.keys())
        return given_column_set.issubset(model_column_set)

    def get_model_columns(self):
        model_column_set = set(
            inspect(self.model).column_attrs.keys()
        )
        model_column_set.remove('id')
        return model_column_set
