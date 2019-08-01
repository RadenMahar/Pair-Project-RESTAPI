# @app.route('/')
# def index():
#     return "<h1> Hello : This main route <h1>"

# @app.route('/name', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
# def name_controller():
#     person = Person()
#     if request.method in 'POST':
#         data = request.get_json()
#         person.name = data['name']
#         person.age = data['umur']
#         person.sex = data['sex']
#         return json.dumps(person.__dict__), 200, {'Content-Type': 'application/json'}
            #json.dumps : json -> text
        
#         #respon code -> 200
#         #json.dumps(person.__dict__) -> text
#         #{'Content-Type': 'application/json'} -> file json

#     elif request.method == 'GET':
#         return json.dumps(person.__dict__), 200, {'Content-Type': 'application/json'}
#     elif request.method == 'PUT':
#         data = request.get_json()
#         person.name = data['name']
#         person.age = data['umur']
#         person.sex = data['sex']
#         return json.dumps(person.__dict__), 200, {'Content-Type': 'application/json'}
    
#     elif request.method == 'DELETE':
#         return 'Deleted', 200
#     else:
#         return 'Not yet implement', 501

# from flask import Flask, request
# import json
from flask_restful import Api
from blueprints import app, manager
import logging, sys
from logging.handlers import RotatingFileHandler
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()



## initiate flask-restful instance
api = Api(app, catch_all_404s=True)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as e:
        formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes = 10000, backupCount=10)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        app.run(debug=True, host='0.0.0.0', port = 7000)