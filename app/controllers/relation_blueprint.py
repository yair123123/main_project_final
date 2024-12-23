from flask import Blueprint, jsonify
from app.dbs.mongodb.repository import most_deadly, average_casualties_by_area, top_5_most_num_spread, \
    most_group_active_by_region, history_events_by_year
from app.dbs.neo4j.repository.relation_repository import groups_with_common_goal_by_region

relation_blueprint = Blueprint('relation', __name__)

@relation_blueprint.route('/')
def index():
    return jsonify({
        "message": "Please enter stat for result!"
    })

@relation_blueprint.route('/most_deadly/<string:country>')
def get_groups_with_common_goal_by_region(country:str):
    try:
        res = groups_with_common_goal_by_region(bool(country))
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/average_casualties_by_area/<string:top>')
def average_casualties(top:str):
    try:
        res = average_casualties_by_area(bool(top))
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/top_5_most_num_spread/')
def get_top_5_most_num_spread():
    try:
        res = top_5_most_num_spread()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/most_group_active_by_region/')
def get_most_group_active_by_region():
    try:
        res = most_group_active_by_region()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/history_events_by_year/<int:year>')
def get_history_events_by_year(year:int):
    try:
        res = history_events_by_year(year)
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

