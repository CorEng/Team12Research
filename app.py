from json import dumps

from flask import Flask, redirect, render_template
from flask import jsonify
from MySQLdb import connect

app = Flask(__name__)

connection = connect('127.0.0.1', 'root', 'abc', 'mydb')


@app.route('/')
def index():
    return render_template()


@app.route('/hello')
def hello():
    return 'hello'


@app.route('/routes/<start>/<end>', methods=['GET'])
def routes(start, end):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT r.route_short_name, t.trip_head_sign, t.direction_id from routes r, trips t, "
                       "stop_times st1, stop_times st2 where r.route_id = t.route_id and t.trip_id = st1.trip_id and "
                       "t.trip_id = st2.trip_id and st1.stop_sequence < st2.stop_sequence and EXISTS ( SELECT * from "
                       f"stops s1 where st1.stop_id = s1.stop_id and s1.stop_name REGEXP %s) and EXISTS ( SELECT * "
                       f"from stops s2 where s2.stop_id = st2.stop_id and s2.stop_name REGEXP %s)", [start, end])

        rows = [row for row in cursor.fetchall()]

        print(rows)
        return jsonify(rows)


@app.route('/arrivals/<route>')
def arrival_time(route):
    data = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT st.arrival_time from routes r, trips t, stop_times st, "
                       "stops where r.route_id = t.route_id and t.trip_id = st.trip_id and r.route_short_name = %s "
                       "and st.stop_sequence = 1 ORDER BY st.arrival_time", [route])
        data = cursor.fetchall()

    return jsonify([row[0].strftime("%H:%M:%S") for row in data])


@app.route('/stops/<route>')
def stops(route):
    trips = []
    data = {}

    with connection.cursor() as cursor:
        #         get the trip_id first
        cursor.execute("SELECT DISTINCT t.trip_id from routes r, trips t where r.route_id = t.route_id and "
                       "r.route_short_name = %s", [route])

        trips = [row[0] for row in cursor.fetchall()]

        for trip in trips:
            cursor.execute("SELECT DISTINCT s.stop_name, st.stop_sequence from stop_times st, stops s where "
                           "st.stop_id = s.stop_id and st.trip_id = %s ORDER by "
                           "st.stop_sequence", [trip])

            data[trip] = [row[0] for row in cursor.fetchall()]

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

# set FLASK_APP=app.py
# set FLASK_ENV=development
