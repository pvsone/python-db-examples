from flask import Flask
from pymongo import MongoClient
import os
import sys
import logging
import json

app = Flask(__name__)

port = int(os.getenv('PORT', 8080))

if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    mongo_env = services['user-provided'][0]['credentials']
else:
    mongo_env = dict(
        server='localhost',
        port='27017',
        database='test'
    )

@app.route('/restaurant')
def restaurant():
    app.logger.info('**** restaurant ****')
    client = MongoClient(mongo_env['server'], int(mongo_env['port']))
    db = client[mongo_env['database']]
    coll = db['restaurants']
    restaurant = coll.find_one()
    name = restaurant['name']

    app.logger.info(name)
    return 'RESTAURANT: ' + name

if __name__ == '__main__':
    ch = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(ch)
    app.logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=port)
