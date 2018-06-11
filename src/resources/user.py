from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

from .models import User
from .schema import user_schema


class UserView(Resource):

    def get(self, user_id):
        try:
            # TODO FAZER NESTED
            user = User.get(id=user_id)
            data = user_schema.dump(user)
            data = jsonify(data)
            data.status_code = 200
        except User.DoesNotExist:
            data = jsonify({"message": "User could not be found"})
            data.status_code = 404

        return data

    def delete(self, user_id):
        q = User.delete().where(User.id == user_id)
        q.execute()
        data = jsonify()
        data.status_code = 204
        return data

    def put(self, user_id):
        json_input = request.get_json()
        # TODO FAZER NESTED

        try:
            user = User.get(id=user_id)
            data = user_schema.load(json_input)
            update = user.update(name=data["name"])
            update.execute()
            data = jsonify(data)
            data.status_code = 201
        except ValidationError as err:
            data = {'errors': err.messages}
            data.status_code = 422

        return data


class UserAdd(Resource):

    def post(self):
        json_input = request.get_json()
        # TODO FAZER NESTED

        try:
            data = user_schema.load(json_input)
            User.create(name=data["name"])
            data = jsonify(data)
            data.status_code = 201
        except ValidationError as err:
            data = {'errors': err.messages}
            data.status_code = 422

        return data
