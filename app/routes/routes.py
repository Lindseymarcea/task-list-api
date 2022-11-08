from flask import Blueprint, make_response, request, jsonify, abort, request
from app import db
from app.models.task import Task
from datetime import datetime
from app.models.goal import Goal

#VALIDATE ID
def validate_id(class_obj,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{class_obj} {id} is an invalid id"}, 400))
    query_result = class_obj.query.get(id)
    if not query_result:
        abort(make_response({"message":f"{class_obj} {id} not found"}, 404))

    return query_result

#CREATE TASK
task_bp = Blueprint("Task", __name__, url_prefix="/tasks")
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task.from_json(request_body)
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"],
                    task_id=None)

    # abort(make_response)  
    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} has been successfully created", 201)

#GET ALL TASKS

@task_bp.route("", methods=["GET"])
def read_all_task():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

#GET ONE TASK
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)
    response_body = {
        "task": task.to_dict()
    }
    return response_body

#UPDATE TASK
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json() 

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"] #not sure if to include this right now
    # task.update(request_body)
    db.session.commit()
    return make_response(f"Task #{task.id} successfully updated")

#DELETE ONE TASK
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task.id} has been successfully deleted")

#GET TASK WITH QUERY PARAMETERS
