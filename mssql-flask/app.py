from flask import Flask
import pymssql
import os
import sys
import logging
import json

app = Flask(__name__)

port = int(os.getenv('PORT', 8080))

if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    mssql_env = services['user-provided'][0]['credentials']
else:
    mssql_env = dict(
        server='hostname',
        user='username',
        password='password',
        database='dbname'
    )

@app.route('/bananas')
def bananas():
    app.logger.info('**** bananas ****')
    conn = pymssql.connect(
        server=mssql_env['server'],
        user=mssql_env['user'],
        password=mssql_env['password'],
        database=mssql_env['database']
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
