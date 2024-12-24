from flask import Blueprint, jsonify, request

elastic_blueprint = Blueprint('elastic', __name__)


@elastic_blueprint.route('/')
def index():
    return jsonify({
        "message": "Please enter stat for result!"
    })


@elastic_blueprint.route('/',methods=['POST'])
def search_news():
    try:
        text = request.json.get('text')
        return jsonify({
            "res": res
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@elastic_blueprint.route('/unique_groups_by_location/<string:country>')
def unique_groups_by_location(country: str):
    try:
        if not bool(country):
            res = unique_groups_by_region()
        else:
            res = unique_groups_by_country()
        return jsonify({
            "res": res
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@elastic_blueprint.route('/shared_goals_in_groups_by_year/<string:year>')
def get_shared_goals_in_groups_by_year(year: str):
    try:
        res = shared_goals_in_groups_by_year(year)
        return jsonify({
            "res": res
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@elastic_blueprint.route('/shared_attack_type_in_groups_by_location/<string:country>')
def get_shared_attack_type_in_groups_by_location(country: str):
    try:
        if not bool(country):
            res = shared_attack_type_in_groups_by_region()
        else:
            res = shared_attack_type_in_groups_by_country()
        return jsonify({
            "res": res
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

