broker_url = "redis://localhost:6379/1"
broker_transport_options = {
    "visibility_timeout": 360,
    "queue_order_strategy": "priority",
}
result_backend = broker_url
accept_content = ["application/json"]
task_serializer = "json"
result_serializer = "json"
broker_connection_retry_on_startup = True
