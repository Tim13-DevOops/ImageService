import os

from flask import Flask
from flask.wrappers import Response
from flask_cors import CORS
import app.config as config
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


cors = CORS(app, resources={r"/*": {"origins": "localhost"}})


@app.route('/')
def index():
    return "hello world"

@app.errorhandler(Exception)
def handle_exception(error):
    response = Response()
    response.data = json.dumps(
        {
            "code": 500,
            "name": "Internal server error",
        }
    )
    response.status_code = 500
    response.content_type = "application/json"
    return response




def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
