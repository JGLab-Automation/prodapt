__author__ = 'JG'

from flask import Blueprint, request, abort, make_response, jsonify
from lib import utility as util
from webapp import services as svc

operations = Blueprint('operations', __name__)

log = util.Log()


@operations.route("/api/v1/prodapt/fetch", methods=['GET'])
def test1():
    status, result = svc.Test().fetch_from_source()
    if status == 'success':
        return make_response(jsonify({'status_code': 200, 'status': status, 'data': result}), 200)
    else:
        abort(503, description=result)


@operations.route("/api/v1/prodapt/<post_id>", methods=['GET'])
def test3(post_id):
    status, result = svc.Test().view_post_details(post_id=post_id)
    if status == 'success':
        return make_response(jsonify({'status_code': 200, 'status': status, 'data': result}), 200)
    elif status == 'failure' and result == 'post_not_found':
        abort(404, description=result)
    else:
        abort(503, description=result)
