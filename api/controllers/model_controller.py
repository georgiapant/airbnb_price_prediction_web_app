import datetime

from flask import Blueprint, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from task_base_logger import logger

task_api = Blueprint(
    name="task_controller", import_name="task_controller", url_prefix="/todo/api/v1.0/tasks"
)

auth = HTTPBasicAuth()

users = {
    "johndoe": generate_password_hash("johndoe"),
    "python": generate_password_hash("my_python")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


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


@task_api.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found. Your fault"}), 404


@task_api.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request. Your fault"}), 400


@task_api.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Unauthorized. You shall not pass"}), 403


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default authy dialog,
    # this way we can handle AUTH errors/exceptions
    return jsonify({'error': 'Unauthorized access'}), 403


@task_api.route('/', methods=['GET'])
@auth.login_required
def get_tasks():
    logger.info(f"Requested tasks from {request.remote_addr}")
    return jsonify({'tasks': tasks})


@task_api.route('/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            logger.info(f"Requested task {task_id} from {request.remote_addr}")
            return jsonify(task)
    logger.error(f"Requested task {task_id} from {request.remote_addr}. Not found")
    abort(404)


@task_api.route('/', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        logger.error(f"Attempted to add task from {request.remote_addr}. Bad request: {request.json}")

        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    logger.info(f"Added task from {request.remote_addr} : {request.json}")
    return jsonify({'task': task}), 201


@task_api.route('/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        logger.error(f"Attempt to update task {task_id} from {request.remote_addr}. Did not found")
        abort(404)
    if not request.json:
        logger.error(f"Attempt to update task {task_id} from {request.remote_addr}. Bad request {request.json}")
        abort(400)
    # The below checks are similar. Can you find a way to write the below code better ?
    if 'title' in request.json and type(request.json['title']) != str:
        logger.error(f"""Attempt to update task {task_id} from {request.remote_addr}. Bad request {request.json}. 
                      Title not string""")
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        logger.error(f"""Attempt to update task {task_id} from {request.remote_addr}. Bad request {request.json}. 
                      description not string""")
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        logger.error(f"""Attempt to update task {task_id} from {request.remote_addr}. Bad request {request.json}. 
                      done not bool""")
        abort(400)

    # Try this with and without copy().
    # When you do not call copy you ll just create a reference to the task[0] object.
    # Check your logs to identify how this affects you.
    task_to_log = task[0].copy()
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    if request.json.get('done') is True and not task[0].get('completed_at'):
        task[0]['completed_at'] = str(datetime.datetime.now())
    if request.json.get('done') is False and task[0].get('completed_at'):
        del task[0]['completed_at']
    task[0]['done'] = request.json.get('done', task[0]['done'])
    logger.info(f"Updated task {task_id}. From {task_to_log} to {task[0]}")
    return jsonify({'task': task[0]})


@task_api.route('/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(list(task)[0])
    return jsonify({'result': True})
