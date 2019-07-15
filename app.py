from flask import Flask, redirect, render_template, request, jsonify
from get_data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/directions", methods=['GET', 'POST'])
def directions():
    postA = request.args.get('postA')
    postB = request.args.get('postB')

    intermediate = Stops()
    get_goo_data = intermediate.get_direct_goo(postA, postB)
    intermediate.fin(get_goo_data)

    return jsonify(get_goo_data)



if __name__ == '__main__':
    app.run(debug=True)



#set FLASK_APP=app.py
#set FLASK_ENV=development