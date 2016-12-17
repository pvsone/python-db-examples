from flask import Flask
import mysql.connector
import os
import sys
import logging
import json

app = Flask(__name__)

port = int(os.getenv('PORT', 8080))

if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    mysql_env = services['p-mysql'][0]['credentials']
else:
    mysql_env = dict(
        username='username',
        password='password',
        hostname='hostname',
        name='dbname'
    )

@app.route('/bananas')
def bananas():
    app.logger.info('**** bananas ****')
    conn = mysql.connector.connect(
        user=mysql_env['username'],
        password=mysql_env['password'],
        host=mysql_env['hostname'],
        database=mysql_env['name']
    )

    cursor = conn.cursor()
    cursor.execute("""
        SELECT quantity
        FROM inventory
        WHERE name = 'banana'
    """)
    row = cursor.fetchone()
    conn.close()
    app.logger.info(row[0])
    return 'BANANAS: ' + str(row[0])

if __name__ == '__main__':
    ch = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(ch)
    app.logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=port)
