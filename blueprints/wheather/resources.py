import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
import requests
from flask_jwt_extended import jwt_required

bp_weather = Blueprint('weather', __name__)

api = Api(bp_weather)


class PublicGetCurrentWeather(Resource):
    wio_host = 'https://api.weatherbit.io/v2.0'
    wio_apikey = '001de4440e814c16bc45197fd601ef9d'

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host + '/ip', params={'ip': args['ip'], 'key': self.wio_apikey})
        geo = rq.json()
        lat = geo['latitude']
        lon = geo['longitude']
        rq = requests.get(self.wio_host + '/current', params={'lat':lat, 'lon': lon, 'key': self.wio_apikey})
        current = rq.json()

        return {
            'city': geo['city'],
            'organization': geo['organization'],
            'timezone': geo['timezone'],
            'current_weather': {
                'date': current['data'][0]['datetime'],
                'temp': current['data'][0]['temp']
            }
        }

api.add_resource(PublicGetCurrentWeather, '', '/public/weather/current')
