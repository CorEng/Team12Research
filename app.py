from flask import Flask, redirect, render_template, request, jsonify
from datetime import datetime, timedelta
from get_data import *

app = Flask(__name__)

@app.route('/')
def index():
    todayObj = datetime.datetime.now()
    today = todayObj.strftime("%Y-%m-%d")
    max = todayObj + timedelta(days=90)
    maxDate = max.strftime("%Y-%m-%d")

    return render_template('index.html', today=today, maxDate=maxDate)

@app.route("/directions", methods=['GET', 'POST'])
def directions():
    postA = request.args.get('postA')
    postB = request.args.get('postB')
    frontDepArr = request.args.get('htmlDepArr')
    frontTime = request.args.get('htmlTime')
    frontDate = request.args.get('htmlDate')


    intermediate = Stops()
    secs = intermediate.getSeconds(frontDate, frontTime)
    get_goo_data = intermediate.get_direct_goo(postA, postB, secs, frontDepArr)
    interStops = intermediate.fin(get_goo_data)
    jsonObj = get_goo_data
    global full
    full = {"interstops": interStops, "gooData": jsonObj}

    return jsonify(full)

@app.route("/amenities", methods=['GET', 'POST'])
def Amenities():
    frontAmenities = request.args.get('htmlAmenities')

    interAmenities = Stops()
    amenitiesList = interAmenities.getAmenities(frontAmenities, full["interstops"])

    return jsonify(amenitiesList)


if __name__ == '__main__':
    app.run(debug=True)


#set FLASK_APP=app.py
#set FLASK_ENV=development