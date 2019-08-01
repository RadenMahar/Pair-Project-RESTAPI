import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Locations
import requests
from flask_jwt_extended import jwt_required

from . import *
from blueprints import db, app
# , internal_required

bp_location = Blueprint('location', __name__)

api = Api(bp_location)


class GetLocation(Resource):
    wio_host = 'https://api.weatherbit.io/v2.0'
    wio_apikey = 'a2e124ae85e749d6b971dd39271c7737'

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host + '/ip', params={'ip': args['ip'], 'key': self.wio_apikey})
        geo = rq.json()
        lat = geo['latitude']
        lon = geo['longitude']
        city = geo['city']
        rq = requests.get(self.wio_host + '/current', params={'lat':lat, 'lon': lon, 'key': self.wio_apikey})
        current = rq.json()


        location = Locations(args['ip'], city, lat, lon)
        db.session.add(location)
        db.session.commit()

        app.logger.debug('DEBUG : %s', location)


        return {
            'city': city,
            'ip': args['ip'],
            'latitude': lat,
            'longitute': lon
        }

api.add_resource(GetLocation, '', '/public')

