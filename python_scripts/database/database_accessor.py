from flask import Flask, request
import requests
import sqlite3
import json

DATABASE = './actuator_states.db'

app = Flask(__name__)

# read in json file for database initialization
new_data = requests.get(url="http://172.17.0.1:4001/config").text
with sqlite3.connect(DATABASE) as db:
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS current_states (actuator PRIMARY KEY, state text)')
    data = json.loads(new_data)
    for key in data.keys():
        if "a" in key:
            cur.execute('INSERT INTO current_states VALUES (\'' + str(key) + '\', \'' + str(data[key]["state"]) + '\')')
            db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def hello():
    return json.dumps({'data': 'hello', 'code': 200})

@app.route('/state', methods=['GET'])
def accessor():
    # get for database queries (ui)
    with sqlite3.connect(DATABASE) as db:
        cur = db.cursor()
        cur.execute('SELECT * FROM current_states')
        states = {}
        for row in cur:
            states[row[0]] = row[1]
    return json.dumps(states)
    
@app.route('/', methods=['POST'])
def updater():
    # post for database updates (used by ui api)
    with sqlite3.connect(DATABASE) as db:
        cur = db.cursor()
        for key in request.form.keys():
            cur.execute('SELECT EXISTS(SELECT * FROM current_states WHERE actuator = \'' + key + '\')')
            exists = 0
            for row in cur:
                exists = row[0]

            if exists == 1:
                cur.execute('UPDATE current_states SET state = \'' + str(request.form[key]) + '\' WHERE actuator = \'' + key + '\'')
                db.commit()
    return "ok"

if __name__=="__main__":
    app.run(host='0.0.0.0', port='4000')
