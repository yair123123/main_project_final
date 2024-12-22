from flask import Blueprint, jsonify
from app.dbs.mongodb.repository import most_deadly, average_casualties_by_area

stat_blueprint = Blueprint('stat', __name__)

@stat_blueprint.route('/')
def index():
    return jsonify({
        "message": "Please enter stat for result!"
    })

@stat_blueprint.route('/most_deadly/<int:top>')
def get_most_deadly(top:int):
    try:
        res = most_deadly(top)
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@stat_blueprint.route('/average_casualties_by_area/<int:top>')
def average_casualties(top:int):
    try:
        res = average_casualties_by_area(top)
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

