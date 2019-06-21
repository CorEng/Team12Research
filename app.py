from flask import Flask, redirect, render_template, request
from get_data import *

app = Flask(__name__)

@app.route('/')
def index():
    lat_lon_stops = []
    return render_template('index.html', lat_lon_stops=lat_lon_stops)

@app.route('/handle_search', methods = ["POST"])
def handle_search():
    stopA = request.form.get("stopA")
    stopB = request.form.get("stopB")
    route = request.form.get("route").upper()
    scroll = "map"

    a = Stops()
    b = a.a_to_b(stopA, stopB, route)
    lat_lon_stops = a.get_searched_stops(b)
    return render_template('index.html', lat_lon_stops=lat_lon_stops, scroll=scroll)


if __name__ == '__main__':
    app.run(debug=True)



#set FLASK_APP=app.py
#set FLASK_ENV=development