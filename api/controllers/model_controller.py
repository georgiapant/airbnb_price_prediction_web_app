import datetime

from flask import Blueprint, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from services import model_service
from base_logger import logger

model_api = Blueprint(
    name="model_controller",
    import_name="model_controller", 
    url_prefix="/api/v1.0/model"
)

@model_api.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found. Your fault"}), 404


@model_api.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request. Your fault"}), 400


@model_api.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Unauthorized. You shall not pass"}), 403

@model_api.errorhandler(500)
def forbidden(error):
    return jsonify({"error": "Internal server error. My fault"}), 403


@model_api.route('/', methods=['POST'])
def model():
    '''
    Check that all fields are filled
    '''
    if not request.json:
        logger.error(f"Attempted to get price from {request.remote_addr}. Bad request: {request.json}")
        abort(400)
    if  'host_id' not in request.json:
        logger.error(f"Id or host Id not provided. Bad request: {request.json}")
        abort(400)
        
    if 'latitude' not in request.json or 'longitude' not in request.json:
        logger.error(f"Latitude or longitude not provided. Bad request: {request.json}")
        abort(400)
        
    if 'room_type' not in request.json or 'minimum_nights' not in request.json or 'accommodates' not in request.json:
        logger.error(f"Room information not provided. Bad request: {request.json}")
        abort(400)
    
    result = model_service.main(request.json)
    
    if not result:
        result = {"price":"Please check your inputs!"}
        # abort(404)
    if result.get('error'):
        abort(500)

    return jsonify(result), 200
