from flask import Flask, Blueprint
from flask_restplus import Resource, Api

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='')
api = Api(blueprint, doc='/doc/', version='1.0', title='Gitlab Badges API',
    description='Because Gitlab does not support it natively, this api generates SVG images as badges that can then be used inside Gitlab',)
app.register_blueprint(blueprint)
# app.config.from_object('config')
from app import server
