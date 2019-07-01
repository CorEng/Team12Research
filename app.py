from flask import Flask, redirect, render_template, request
from get_data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/directions", methods=['GET', 'POST'])
def directions():
    postA = request.args.get('postA')
    postB = request.args.get('postB')

    # print(Stops().get_direct_goo(postA, postB))
    return "HELLO"



if __name__ == '__main__':
    app.run(debug=True)



#set FLASK_APP=app.py
#set FLASK_ENV=development