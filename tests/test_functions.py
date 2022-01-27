
import json

from flask_todo_app import app


def test_add_todo():

    task = {
        "task": "prepare for exam",
        "completed": 0
    }
    response = app.test_client().post('/todo', data=json.dumps(task),
                                      content_type='application/json')
    assert response.status_code == 200


def test_get_todo():

    todo_id = 2
    response = app.test_client().get(f'/todos?todo_id={todo_id}')
    assert response.status_code == 200


def test_update_todo():

    task = {
        "todo_id": 1,
        "task": "prepare for exam",
        "completed": 1
    }

    response = app.test_client().post('/todo', data=json.dumps(task),
                                      content_type='application/json')
    assert response.status_code == 200
