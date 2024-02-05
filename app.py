from flask import Flask, request, render_template
from flask_cors import CORS
from backend import *
import os, secrets
app = Flask(__name__)
CORS(app)

# Directory Path of current file 
source_path = os.path.dirname(__file__)
source_path = str(source_path)

# Configuration for Flask App
app._static_folder = "templates/static/"
app.secret_key = secrets.token_hex(16)


# Index Page
@app.route('/')
def main_page():
    return fetch_task()


# Add Tasks
@app.route('/add')
def add_page():
    return render_template('add.html')

@app.route('/api/v1/add/task', methods=["POST"])
def add_tasks():
    return add_task()

@app.route("/api/v1/update/task", methods=["POST"])
def update_backend():
    form = request.form
    serial_no = form['serial']
    print(serial_no)
    # serial_no = request.args.get('')
    # request_json = request.get_json()
    try:
        message, statuscode = update_task(serial=serial_no)
        return f"<h1>{message['message']}</h1>", statuscode
    except Exception as err:
        return {'returncode': 1, 'message': f'{err}'}, 503


@app.route("/test")
def test():
    return "<h1> Test Approved From Back-End </h1>"


if __name__ == "__main__":
    app.run(debug=True)