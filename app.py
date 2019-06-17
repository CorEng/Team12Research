from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template()



if __name__ == '__main__':
    app.run(debug=True)



#set FLASK_APP=app.py
#set FLASK_ENV=development