from data import users
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


'''
    Define a resource class to create an API endpoint.
    Methods within this resource are mapped to a specific HTTP request (get, post, delete...)
    Thus, each method indicates the intended action to performed.
    Each method will also return an appropriate HTTP response status code (200, 404...)
    to indicate how the request has been processed
'''


class User(Resource):

    #  get will retrieve info on person with passed name (request for info from specified resource)
    #  if name is in our data, return info + 200 for successful request (ok)
    #  if name not found, return 404 error
    def get(self, name):
        for user in users:
            if name == user['name']:
                return user, 200
            return "User not found", 404

    #  post will create a new user into our data (request to create new resource)
    #  the request here would have the arguments needed in the request's body as JSON
    #  thus we use a parser, add the arguments to it, then parse through the request to map everything correctly
    #  we then create the user using the parsed arguments to fill in the info of the user
    #  if user with the name exists already, return 404 error
    #  otherwise we add to our data users & return the new user's info + 201 created
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('age')
        parser.add_argument('occupation')
        args = parser.parse_args()

        for user in users:
            if name == user['name']:
                return f"User with name {name} already exists", 400

        user = {
            'name': name,
            'age': args['age'],
            'occupation': args['occupation']
        }

        users.append(user)
        return user, 201

    #  put will update the info of the user with the passed name (request to modify existing resource)
    #  if user does not exist, we create a new user (so same as post here), user + 201 created
    #  otherwise, we update and return the user + 200 ok
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('age')
        parser.add_argument('occupation')
        args = parser.parse_args()

        for user in users:
            if name == users['name']:
                user['age'] = args['age']
                user['occupation'] = args['occupation']
                return user, 200

        user = {
            'name': name,
            'age': args['age'],
            'occupation': args['occupation']
        }

        users.append(user)
        return user, 201

    #  deletes user with name passed in from our data (request to remove a resource)
    def delete(self, name):
        global users
        users = [user for user in users if user['name'] != name]
        return f'{name} is deleted', 200


class Users(Resource):

    def get(self):
        return users, 200


api.add_resource(Users, "/users")
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
