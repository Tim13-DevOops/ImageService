import os
from pathlib import Path

from flask import Flask, request, jsonify, abort, Response
from flask_cors import CORS
import uuid
from flask.helpers import send_from_directory
from prometheus_flask_exporter import PrometheusMetrics
import json

image_directory = 'public/images'
Path(f'{image_directory}').mkdir(parents=True, exist_ok=True)

app = Flask(__name__,  static_url_path='/public')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
metrics = PrometheusMetrics(app)


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

from prometheus_metrics.prometheus_metrics import (
    counter_ingress, counter_egress, counter_404
)

metrics.register_default(
    metrics.counter(
        "flask_user_counter",
        "Number of visits by unique users",
        labels={
            "service": lambda: "image_service",
            "ip_address": lambda: request.remote_addr,
            "browser": lambda: request.user_agent.browser,
        },
    )
)

metrics.register_default(
    metrics.counter(
        "flask_by_endpoint_counter",
        "Number of requests per endpoint",
        labels={
            "service": lambda: "image_service",
            "path": lambda: request.path,
            "status_code": lambda response: response.status_code,
        },
    )
)

@app.errorhandler(404)
def page_not_found(e):
    counter_404.labels(service="image_service", endpoint=request.path).inc()
    return e, 404

@app.before_request
def count_size_ingress():
    if request.content_length:
        counter_ingress.labels(service="image_service").inc(
            request.content_length / 1024 / 1024
        )

@app.after_request
def count_size_egress(response):
    if response.content_length:
        counter_egress.labels(service="image_service").inc(
            response.content_length / 1024 / 1024
        )
    return response

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
