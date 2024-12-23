from flask import Blueprint, jsonify

from app.dbs.neo4j.repository.relation_repository import groups_with_common_goal_by_region, \
    groups_with_common_goal_by_country, both_groups_in_event_by_country, both_groups_in_event_by_region, \
    shared_goals_in_groups_by_year, shared_attack_type_in_groups_by_region, shared_attack_type_in_groups_by_country

relation_blueprint = Blueprint('relation', __name__)

@relation_blueprint.route('/')
def index():
    return jsonify({
        "message": "Please enter stat for result!"
    })

@relation_blueprint.route('/groups_with_common_goal_by_location/<string:country>')
def get_groups_with_common_goal_by_location(country:str):
    try:
        if not bool(country):
            res = groups_with_common_goal_by_region()
        else:
            res = groups_with_common_goal_by_country()
        return jsonify({
            "res": res
        }),200

    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/both_groups_in_event_by_location/<string:country>')
def get_both_groups_in_event_by_location(country:str):
    try:
        if not bool(country):
            res = both_groups_in_event_by_region()
        else:
            res = both_groups_in_event_by_country()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/shared_goals_in_groups_by_year/')
def get_shared_goals_in_groups_by_year():
    try:
        res = shared_goals_in_groups_by_year()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@relation_blueprint.route('/shared_attack_type_in_groups_by_location/')
def get_shared_attack_type_in_groups_by_location(country:str):
    try:
        if not bool(country):
            res = shared_attack_type_in_groups_by_region()
        else:
            res = shared_attack_type_in_groups_by_country()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

# @relation_blueprint.route('/history_events_by_year/<int:year>')
# def get_history_events_by_year(year:int):
#     try:
#         res = history_events_by_year(year)
#         return jsonify({
#             "res": res
#         }),200
#     except Exception as e:
#         return jsonify({"message":str(e)}),500

