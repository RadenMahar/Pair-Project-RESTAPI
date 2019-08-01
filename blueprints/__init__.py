from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
import requests

app = Flask(__name__)

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/rest_training'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.config['JWT_SECRET_KEY'] = 'Skjakdjladd668adkka'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

#jwt custom decorator admin
def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:
            return {'status':'forbidden', 'message':'internal only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception:
        requestData = request.args.to_dict()
    
    if response.status_code > 200:
        app.logger.error("REQUEST_LOG\t%s", 
            json.dumps({
            'method': request.method, 
            'code': response.status,
            'uri': request.full_path, 
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))}))
        return response
    else:
        app.logger.warning("REQUEST_LOG\t%s", 
            json.dumps({
            'method': request.method, 
            'code': response.status,
            'uri': request.full_path, 
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))}))
        return response
        # if request.method == 'GET':
        #     app.logger.warning("REQUEST_LOG\t%s", json.dumps({'uri': request.full_path,'request':request.args.to_dict(), 'response': json.loads(response.data.decode('utf-8'))
        #         }))
        # else:
        #     app.logger.warning("REQUEST_LOG\t%s", json.dumps({'uri': request.full_path,'request':request.get_json(), 'response': json.loads(response.data.decode('utf-8'))}))
    # return response

#result of json.load -> is dictionary
#result of json.dumps -> is string



from blueprints.Client.resources import bp_client
from blueprints.auth import bp_auth
from blueprints.wheather.resources import bp_weather


app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_weather, url_prefix='/weather')
db.create_all()
