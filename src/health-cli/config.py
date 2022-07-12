VERSION = "0.0.1"
FILE_TYPE = {
    "JSON": "json"
}
SERVICE_TYPE = {
    "REDIS": "redis",
    "MYSQL": "mysql",
    "INFLUXDB": "influxdb",
    "RABBIT_MQ": "rabbit_mq",
    "REST_API": "rest_api"
}
REQUEST_METHOD = {
    "GET": "GET",
    "PUT": "PUT",
    "POST": "POST",
    "DELETE": "DELETE"
}
CONFIG_FIELD_REQUIRED = [{"name": "services", "type": list}]
CONFIG_SERVICE_FIELD_REQUIRED = [{"name": "name", "type": str}, {"name": "type", "type": str}, {"name": "timeout", "type": int}, {"name": "retry", "type": int}]