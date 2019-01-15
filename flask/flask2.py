from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask import abort
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

app = Flask(__name__)
api = Api(app)


class UserAPI(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(UserAPI, '/users', endpoint='user')


class TaskListAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        return jsonify({'tasks': tasks})

    def post(self):
        pass


class TaskAPI(Resource):
    decorators = [auth.login_required]
    def get(self, id):
        task = [t for t in tasks if t['id'] == id]
        if len(task) == 0:
            abort(404)
        return jsonify({'task': task[0]})

api.add_resource(TaskListAPI, '/app', endpoint='tasks')
api.add_resource(TaskAPI, '/app/<int:id>', endpoint='task')




if __name__ == '__main__':
    app.run(debug=True)
