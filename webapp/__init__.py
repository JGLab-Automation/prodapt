__author__ = 'JG'

from flask import Flask, session


def api():
    app = Flask(__name__)

    from webapp.ops.routes import operations
    # from webapp.err.routes import errors

    app.register_blueprint(operations)
    # app.register_blueprint(errors)

    return app
