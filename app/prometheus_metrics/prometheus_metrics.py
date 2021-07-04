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

def init_metrics():
    from app import metrics

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


