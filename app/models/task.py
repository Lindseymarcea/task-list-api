from app import db
from flask import Blueprint, make_response, request, jsonify, abort, request


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None,
            "id": self.task_id
        }

    @classmethod
    def from_json(cls, req_body):
        return cls(
            title=req_body['title'],
            description=req_body['description'],
            completed_at=req_body['completed_at']
        )

    def update(self,req_body):
        try:
            self.title = req_body["title"]
            self.description = req_body["description"]
            self.completed_at = req_body["completed_at"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))