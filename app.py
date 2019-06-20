from flask import Flask, redirect, render_template, request
from get_data import *

app = Flask(__name__)

@app.route('/')
def index():
    a = Stops()
    lat_lon_stops = a.get_stops()
    return render_template('index.html', lat_lon_stops=lat_lon_stops)

@app.route('/handle_search', methods = ["POST"])
def get_search():
    stopA = request.form.get("stopA")
    stopB = request.form.get("stopB")

    a = Stops()
    print(a.a_to_b(stopA, stopB))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)



#set FLASK_APP=app.py
#set FLASK_ENV=development