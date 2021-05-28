__author__ = 'JG'

import os
from flask import Blueprint, make_response, jsonify
from lib import utility as util

errors = Blueprint('errors', __name__)

log = util.Log()


@errors.app_errorhandler(400)
def error_400(err):
    log.error(f"{err.description}")
    return make_response(jsonify({'status_code': 400, 'status': err,
                                  'data': None,
                                  'isShowToaster': True, 'message': err.description}), 400)


@errors.app_errorhandler(401)
def error_401(err):
    log.error(f"{err.description}")
    return make_response(jsonify({'status_code': 401, 'status': err.description,
                                  'data': None,
                                  'isShowToaster': False, 'message': err.description}), 401)


@errors.app_errorhandler(404)
def error_404(err):
    log.error(f"{err.description}")
    return make_response(jsonify({'status_code': 404, 'status': err.description,
                                  'data': None,
                                  'isShowToaster': False, 'message': err.description}), 404)


@errors.app_errorhandler(409)
def error_409(err):
    log.error(f"{err.description}")
    return make_response(jsonify({'status_code': 409, 'status': err.description,
                                  'data': None,
                                  'isShowToaster': False, 'message': err.description}), 409)


@errors.app_errorhandler(502)
def error_502(err):
    log.error(f"{err.description}")
    return make_response(jsonify({'status_code': 502, 'status': err.description,
                                  'data': None,
                                  'isShowToaster': False, 'message': err.description}), 502)


@errors.app_errorhandler(503)
def error_503(err):
    log.error(f"{err.description}")
    return make_response(jsonify({'status_code': 503, 'status': err.description,
                                  'data': None,
                                  'isShowToaster': False, 'message': err.description}), 503)