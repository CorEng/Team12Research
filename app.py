from flask import Flask, redirect, render_template, request
from get_data import *

app = Flask(__name__)

@app.route('/')
def index():
    lat_lon_stops = []
    num_name = Stops().get_all_stops()
    return render_template('index.html', lat_lon_stops=lat_lon_stops, num_name=num_name)


if __name__ == '__main__':
    app.run(debug=True)



#set FLASK_APP=app.py
#set FLASK_ENV=development