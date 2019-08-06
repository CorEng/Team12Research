from flask import Flask, redirect, render_template, request, jsonify
from datetime import datetime
from get_data import *

app = Flask(__name__)


@app.route('/')
def index():
    today_obj = datetime.datetime.now()
    today = today_obj.strftime("%Y-%m-%d")
    max_days = today_obj + timedelta(days=30)
    max_date = max_days.strftime("%Y-%m-%d")

    return render_template('index.html', today=today, maxDate=max_date)


@app.route("/directions", methods=['GET', 'POST'])
def directions():
    post_a = request.args.get('postA')
    post_b = request.args.get('postB')
    front_dep_arr = request.args.get('htmlDepArr')
    front_time = request.args.get('htmlTime')
    front_date = request.args.get('htmlDate')

    intermediate = Stops()
    secs = intermediate.get_seconds(front_date, front_time)
    get_goo_data = intermediate.get_direct_goo(post_a, post_b, secs, front_dep_arr)
    inter_stops = intermediate.fin(get_goo_data)
    json_obj = get_goo_data
    global full
    # notifications = intermediate.notification_check(json_obj)

    # full = {"interstops": inter_stops, "gooData": json_obj, "disruptions": notifications}
    full = {"interstops": inter_stops, "gooData": json_obj}
    return jsonify(full)


@app.route("/amenities", methods=['GET', 'POST'])
def amenities():
    front_amenities = request.args.get('htmlAmenities')

    inter_amenities = Stops()
    amenities_list = inter_amenities.get_amenities(front_amenities, full["interstops"])

    return jsonify(amenities_list)


if __name__ == '__main__':
    app.run(debug=True)

# set FLASK_APP=app.py
# set FLASK_ENV=development
