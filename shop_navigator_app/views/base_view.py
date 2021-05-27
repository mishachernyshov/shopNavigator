from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError

from .. import db


class BaseView(Resource):
    def __init__(self, schema, model):
        self.schema = schema()
        self.model = model

    def get(self, id=None):
        if id:
            return self.get_single_instance(id)
        model_instances = db.session.query(self.model).all()
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
        db.session.add(new_instance)
        db.session.commit()
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
        db.session.add(model_instance)
        db.session.commit()
        return self.schema.dump(model_instance), 200

    def patch(self, id):
        model_instance = db.session.query(self.model) \
            .filter_by(id=id)
        if not model_instance:
            return jsonify({}), 404
        updated_data = request.json
        model_instance.update(updated_data)
        db.session.commit()
        return self.schema.dump(model_instance), 200

    def delete(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return jsonify({}), 404
        db.session.delete(model_instance)
        db.session.commit()
        return {}, 204

    def get_single_instance(self, id):
        model_instance = self.get_model_instance(id)
        if not model_instance:
            return jsonify({}), 404
        return self.schema.dump(model_instance), 200

    def get_model_instance(self, id):
        return db.session.query(self.model) \
            .filter_by(id=id).first()
