from flask import Blueprint, jsonify
from services import stats_service

api = Blueprint(
    name="stats_controller",
    import_name="stats_controller",
    url_prefix="/emp/api/v1/stats",
)


@api.route("/")
def stats():
    return (stats_service.main()), 200
