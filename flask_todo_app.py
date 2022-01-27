from crypt import methods
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)


@app.route("/todo", methods=['POST'])
def addtodo():

    try:
        parser = reqparse.RequestParser()
        parser.add_argument('task', required=True)
        parser.add_argument('completed', required=True)
        args = parser.parse_args()
        task_completed = int(args['completed'])
        new_todo = Todo(task=args['task'], completed=task_completed)
        db.session.add(new_todo)
        db.session.commit()
    except:
        return {"error": "something went wrong"}, 500
    return {"success": "todo added"}, 200


@app.route("/todos", methods=['GET'])
def gettodo():
    args = request.args
    todo_id = args['todo_id']
    try:
        todo = Todo.query.get(int(todo_id))
        print(todo)
        return {
            "name": todo.task,
            "completed": todo.completed
        }, 200
    except:
        return {"error": "something went wrong"}, 500


@app.route("/updatetodo", methods=["PUT"])
def updatetodo():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('task', required=True)
        parser.add_argument('completed', required=True)
        args = parser.parse_args()
        todo = db.session.query(Todo).get(int(args['id']))
        todo.task = args['task']
        todo.completed = int(args['completed'])
        db.session.commit()
        return {
            "success": "todo updated"
        }, 200
    except:
        return {"error": "Something went wrong"}, 500


if __name__ == '__main__':
    app.run(debug=True)
