from flask import Blueprint, jsonify, request

from app.flow.elastic_service import get_news_from_elastic, get_all_from_elastic, get_history_from_elastic, \
    get_all_from_elastic_by_date

elastic_blueprint = Blueprint('elastic', __name__)


@elastic_blueprint.route('/')
def index():
    return jsonify({
        "message": "Please enter stat for result!"
    })


@elastic_blueprint.route('/news/<text>', methods=['GET'])
def search_news(text: str):
    try:
        res = get_news_from_elastic(text)
        return jsonify({
            "res": res
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@elastic_blueprint.route('/all_csv/<string:text>')
def search_all_csv(text: str):
    try:
        res = get_all_from_elastic(text)

        return jsonify({
            "res": res
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@elastic_blueprint.route('/history_csv/<string:text>')
def search_history_csv(text: str):
    try:
        res = get_history_from_elastic(text)
        return jsonify({
            "res": res
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@elastic_blueprint.route('/all_csv_by_date/<string:text>')
def search_all_csv_by_date(text: str):
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        res = get_all_from_elastic_by_date(text, start, end)
        return jsonify({
            "res": res
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
