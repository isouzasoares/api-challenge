from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

from .models import User
from .schema import user_schema


# Todo
Users = {
    '1': {
        'name': 'Fulano Beltrano',
        'forecast': [
            {
                'address': 'Rua Marshmallow',
                'period': {
                    'from': '08:00',
                    'to': '19:00'
                },
                'days': {
                    'sunday': True,
                    'monday': True,
                    'tuesday': True,
                    'wednesday': True,
                    'thursday': True,
                    'friday': False,
                    'saturday': False
                },
                'notification': '07:00'
            }
        ]
    },
    '2': {
        'name': 'Ciclano Beltrano',
        'forecast': [
            {
                'address': 'Rua Oreo',
                'period': {
                    'from': '22:00',
                    'to': '06:00'
                },
                'days': {
                    'sunday': True,
                    'monday': True,
                    'tuesday': True,
                    'wednesday': True,
                    'thursday': True,
                    'friday': False,
                    'saturday': False
                },
                'notification': '21:00'
            }
        ]
    }
}


class UserView(Resource):

    def get(self, user_id):
        try:
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

        try:
            data = user_schema.load(json_input)
            User.create(name=data["name"])
            data = jsonify(data)
            data.status_code = 201
        except ValidationError as err:
            data = {'errors': err.messages}
            data.status_code = 422

        return data
