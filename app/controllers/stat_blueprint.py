from flask import Blueprint, jsonify
from app.dbs.mongodb.repository import most_deadly, average_casualties_by_area, top_5_most_num_spread, \
    most_group_active_by_region, history_events_by_year

stat_blueprint = Blueprint('stat', __name__)

@stat_blueprint.route('/')
def index():
    return jsonify({
        "message": "Please enter stat for result!"
    })

@stat_blueprint.route('/most_deadly/<top>')
def get_most_deadly(top:str):
    try:
        res = most_deadly(bool(top))
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@stat_blueprint.route('/average_casualties_by_area/<string:top>')
def average_casualties(top:str):
    try:
        res = average_casualties_by_area(bool(top))
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        print(e)
        return jsonify({"message":str(e)}),500

@stat_blueprint.route('/top_5_most_num_spread/')
def get_top_5_most_num_spread():
    try:
        res = top_5_most_num_spread()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@stat_blueprint.route('/most_group_active_by_region/')
def get_most_group_active_by_region():
    try:
        res = most_group_active_by_region()
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

@stat_blueprint.route('/history_events_by_year/<int:year>',methods=['GET'])
def get_history_events_by_year(year:int):
    try:
        res = history_events_by_year(year)
        res = [(float(l["location"]["latitude"]),float(l["location"]["longitude"])) for l in res]
        print(res)
        return jsonify({
            "res": res
        }),200
    except Exception as e:
        return jsonify({"message":str(e)}),500

