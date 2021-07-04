from flask import request
from prometheus_client import Counter


counter_404 = Counter(
    "flask_404_counter",
    "Counts number of requests with status code 404 for each endpoint",
    ["service", "endpoint"],
)

counter_ingress = Counter(
    "flask_ingress_counter",
    "Counts the amount of inbound data in the app",
    ["service"],
)


counter_egress = Counter(
    "flask_egress_counter",
    "Counts the amount of outbound data in the app",
    ["service"],
)
