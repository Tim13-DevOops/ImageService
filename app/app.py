import os
from pathlib import Path

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import uuid
from flask.helpers import send_from_directory


image_directory = 'public/images'
Path(f'{image_directory}').mkdir(parents=True, exist_ok=True)

app = Flask(__name__,  static_url_path='/public')
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/image/<imageId>')
def send_file(imageId):
    print(imageId)
    return send_from_directory(f'{image_directory}', imageId)

    
@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    
    if uploaded_file.filename == '':
        abort(400, 'Please select a file to upload')
    print(uploaded_file)
    uploaded_file_name = f'{uuid.uuid4()}.{uploaded_file.filename.split(".")[1]}'
    uploaded_file.save(f'{image_directory}/{uploaded_file_name}')
    return jsonify({'file_name': uploaded_file_name})

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
