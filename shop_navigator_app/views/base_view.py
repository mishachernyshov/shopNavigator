from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError

from shop_navigator_app import db


class BaseView(Resource):
    def __init__(self, schema, service):
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
        try:
            new_instance = self.schema.load(
                request_json, session=db.session
            )
        except ValidationError as e:
            return {'message': str(e)}, 400
        self.service().insert_new_instance(db.session, new_instance)
        return self.schema.dump(new_instance), 201

    def put(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return jsonify({}), 404
        try:
            model_instance = self.schema.load(
                request.json, instance=model_instance,
                session=db.session
            )
        except ValidationError as e:
            return {'message': str(e)}, 400
        self.service().insert_new_instance(db.session, model_instance)
        return self.schema.dump(model_instance), 200

    def patch(self, id):
        model_instance = self.service().get_all_instances_by_id(
            db.session, id
        )
        if not model_instance:
            return jsonify({}), 404
        updated_data = request.json
        self.service.update_instance(
            db.session, model_instance, updated_data
        )
        return self.schema.dump(model_instance), 200

    def delete(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return jsonify({}), 404
        self.service.delete_instance(db.session, model_instance)
        return {}, 204

    def get_single_instance(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return jsonify({}), 404
        return self.schema.dump(model_instance), 200

    def get_model_instance(self, id):
        return self.service().get_first_instance_by_id(db.session, id)
